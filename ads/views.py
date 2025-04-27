# views.py
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Ad, AdInteraction
from .serializers import AdSerializer, AdCreateSerializer
from users.permissions import IsRealAdmin, IsClient, IsAdminOrClient, IsOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated
from .models import RechargeRecord
from .serializers import RechargeRecordSerializer
from rest_framework import status

class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()  # 确保定义 .queryset

    def get_queryset(self):
        # 动态查询集：根据用户角色返回不同的广告
        if self.request.user.role == 'admin':
            return Ad.objects.all()  # 管理员能查看所有广告
        return Ad.objects.filter(advertiser=self.request.user)  # 客户只能查看自己的广告

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [IsOwnerOrAdmin()]  # 使用 IsOwnerOrAdmin 权限类
        elif self.action in ['approve', 'reject']:
            return [IsRealAdmin()]
        elif self.action in ['list', 'retrieve']:
            return [IsAdminOrClient()]
        return [IsAuthenticated()]  # fallback，保险起见

    def get_serializer_class(self):
        if self.action == 'create':
            return AdCreateSerializer
        return AdSerializer

    def perform_create(self, serializer):
        serializer.save(advertiser=self.request.user)

    # 管理员审核广告
    @action(detail=True, methods=['patch'], permission_classes=[IsRealAdmin])
    def approve(self, request, pk=None):
        ad = self.get_object()
        ad.status = 'approved'
        ad.save()
        return Response({'status': 'approved'})

    @action(detail=True, methods=['patch'], permission_classes=[IsRealAdmin])
    def reject(self, request, pk=None):
        ad = self.get_object()
        ad.status = 'rejected'
        ad.reason_rejected = request.data.get('reason', '')
        ad.save()
        return Response({'status': 'rejected', 'reason': ad.reason_rejected})

    # 客户只能删除未审核的广告
    @action(detail=True, methods=['delete'], permission_classes=[IsClient])
    def delete_ad(self, request, pk=None):
        ad = self.get_object()
        if ad.status == 'pending':
            ad.delete()
            return Response({'status': 'deleted'})
        return Response({'status': 'error', 'message': 'Cannot delete approved or rejected ad'}, status=400)

    @action(detail=True, methods=['get'])
    def show(self, request, pk=None):
        """当广告被展示时，展示次数 +1，并判断是否扣费（CPM 模式）"""
        ad = self.get_object()

        if not ad.is_active:
            return Response({'message': '广告已暂停'}, status=status.HTTP_400_BAD_REQUEST)

        ad.display_count += 1

        # ✨ 创建展示记录
        interaction = AdInteraction.objects.create(
            ad=ad,
            user=request.user if request.user.is_authenticated else None,
            action='display'
        )

        # ✅ CPM 扣费逻辑
        if ad.billing_method == 'CPM':
            # 计算每次展示的费用（CPM / 1000）
            cost_per_impression = ad.cpm_price / 1000
            advertiser = ad.advertiser

            if advertiser.balance >= cost_per_impression:
                # 🪙 扣费并保存
                advertiser.balance -= cost_per_impression
                advertiser.save()

                ad.total_spent += cost_per_impression
                ad.save()
            else:
                # ❌ 余额不足，暂停广告
                ad.is_active = False
                ad.save()
                return Response({
                    'message': '余额不足，广告已暂停',
                    'display_count': ad.display_count,
                    'balance': advertiser.balance,
                    'ad_status': 'paused'
                }, status=status.HTTP_402_PAYMENT_REQUIRED)

        else:
            ad.save()

        return Response({
            'message': 'Ad displayed',
            'display_count': ad.display_count,
            'interaction': {
                'id': interaction.id,
                'user': interaction.user.username if interaction.user else 'Anonymous',
                'action': interaction.action,
                'timestamp': interaction.timestamp,
            },
            'balance': ad.advertiser.balance,
            'billing': ad.billing_method,
            'ad_status': 'active' if ad.is_active else 'paused'
        })

    @action(detail=True, methods=['post'])
    def click(self, request, pk=None):
        """当广告被点击时，点击次数 +1，并判断是否扣费（CPC 模式）"""
        ad = self.get_object()

        if not ad.is_active:
            return Response({'message': '广告已暂停'}, status=status.HTTP_400_BAD_REQUEST)

        ad.click_count += 1

        # ✨ 创建点击记录
        interaction = AdInteraction.objects.create(
            ad=ad,
            user=request.user if request.user.is_authenticated else None,
            action='click'
        )

        # ✅ CPC 扣费逻辑
        if ad.billing_method == 'CPC':
            cost_per_click = ad.cpc_price
            advertiser = ad.advertiser

            if advertiser.balance >= cost_per_click:
                # 🪙 扣费并保存
                advertiser.balance -= cost_per_click
                advertiser.save()

                ad.total_spent += cost_per_click
                ad.save()
            else:
                # ❌ 余额不足，暂停广告
                ad.is_active = False
                ad.save()
                return Response({
                    'message': '余额不足，广告已暂停',
                    'click_count': ad.click_count,
                    'balance': advertiser.balance,
                    'ad_status': 'paused'
                }, status=status.HTTP_402_PAYMENT_REQUIRED)

        else:
            ad.save()

        return Response({
            'message': 'Ad clicked',
            'click_count': ad.click_count,
            'interaction': {
                'id': interaction.id,
                'user': interaction.user.username if interaction.user else 'Anonymous',
                'action': interaction.action,
                'timestamp': interaction.timestamp,
            },
            'balance': ad.advertiser.balance,
            'billing': ad.billing_method,
            'ad_status': 'active' if ad.is_active else 'paused'
        })

    @action(detail=True, methods=['post'])
    def play(self, request, pk=None):
        """
        当广告被播放（视频播放等）时，根据播放时长进行扣费（CPT 模式）
        """
        ad = self.get_object()

        if not ad.is_active:
            return Response({'message': '广告已暂停'}, status=status.HTTP_400_BAD_REQUEST)

        # 从请求中获取播放时长（秒）
        duration = int(request.data.get('duration', 0))  # eg: 12 表示播放了12秒
        if duration <= 0:
            return Response({'message': '播放时长必须大于0'}, status=status.HTTP_400_BAD_REQUEST)

        interaction = AdInteraction.objects.create(
            ad=ad,
            user=request.user if request.user.is_authenticated else None,
            action='play',
            duration=duration
        )

        # ✅ CPT 扣费逻辑
        if ad.billing_method == 'CPT':
            seconds_per_unit = 10  # 多少秒作为一个计费单位
            unit_price = ad.cpt_price  # 每单位多少元

            units = duration // seconds_per_unit
            if units <= 0:
                return Response({'message': '播放时长太短，未触发扣费'}, status=status.HTTP_200_OK)

            total_cost = units * unit_price
            advertiser = ad.advertiser

            if advertiser.balance >= total_cost:
                # 🪙 扣费
                advertiser.balance -= total_cost
                advertiser.save()

                ad.total_spent += total_cost
                ad.save()
            else:
                # ❌ 余额不足，暂停广告
                ad.is_active = False
                ad.save()
                return Response({
                    'message': '余额不足，广告已暂停',
                    'play_duration': duration,
                    'charged_units': units,
                    'cost': float(total_cost),
                    'balance': float(advertiser.balance),
                    'ad_status': 'paused'
                }, status=status.HTTP_402_PAYMENT_REQUIRED)

        return Response({
            'message': 'Ad played',
            'play_duration': duration,
            'charged_units': units,
            'cost': float(total_cost),
            'balance': float(ad.advertiser.balance),
            'interaction': {
                'id': interaction.id,
                'user': interaction.user.username if interaction.user else 'Anonymous',
                'action': interaction.action,
                'timestamp': interaction.timestamp,
                'duration': interaction.duration
            },
            'ad_status': 'active' if ad.is_active else 'paused'
        })

class RechargeRecordViewSet(viewsets.ModelViewSet):
    queryset = RechargeRecord.objects.all().order_by('-created_at')
    serializer_class = RechargeRecordSerializer
    
    def get_permissions(self):
        # 根据操作类型来设置权限
        if self.action == 'list':
            # 只有 admin 用户有权限查看所有充值记录
            return [IsRealAdmin()]
        elif self.action == 'create':
            # 只有客户（client）才有权限创建充值记录
            return [IsClient()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        user = self.request.user
        amount = serializer.validated_data['amount']

        # 充值成功后增加用户余额
        user.balance += amount
        user.save()

        # 保存充值记录，并设置状态为成功
        serializer.save(user=user, status='success')

