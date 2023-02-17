from datetime import date, datetime
from main.push_helper import PushHelper
from rest_framework import generics, permissions, viewsets, mixins
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.db.models import Q

from .models import *
from .serializers import *
from .service import *
from .helpers import ConstantsCustom



#Auth
#Create user
class CreateUser(APIView):
    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        phone = request.data.get('phone')
        city = request.data.get('city')
        custom_token = request.data.get('custom_token')
        if name and city and phone and custom_token == ConstantsCustom.custom_token:
            is_same_user = User.objects.filter(phone=phone).exists()
            if is_same_user:
                return Response({
                    'success': False,
                    'detail': 'Клиент с таким номером уже существует'
                }, status=400)
            else:
                new_user = User()
                new_user.phone = phone
                new_user.username = name
                new_user.city = city
                new_user.save()
                return Response({
                    'success': True,
                    'phone': phone,
                    'detail': 'Успешно создали клиента'
                }, 
                status=201)

        else:
            return Response({
                'success': False,
                'detail': 'Вы не предоставили данные'
            }, status=400)


#Login user
class LoginUser(APIView):
    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        password = request.data.get('password')
        if password and phone:
            is_same_user = User.objects.filter(phone=phone).exists()
            if is_same_user == False:
                return Response({
                    'success': False,
                    'detail': 'Аккаунта с таким номером не существует'
                }, status=400)

            user_by_phone = User.objects.get(phone=phone)

            if user_by_phone.registered == True:
                if user_by_phone.check_password(password) == False:
                    return Response({
                        'success': False,
                        'detail': 'Введенные данные не корректны'
                    }, status=400)

                new_token = None
                token_old_or_new, token_old_or_new_created = Token.objects.get_or_create(user=user_by_phone)

                # If token exists: delete old token and then create new
                if token_old_or_new_created == False:
                    print('Token already created')
                    token_old_or_new.delete()
                    token, created = Token.objects.get_or_create(user=user_by_phone)
                    new_token = token
                else:
                    print('Token first created')
                    new_token = token_old_or_new

                return Response({
                    'success': True,
                    'detail': 'Успешно зашли',
                    'token': new_token.key,
                }, status=200)
            else:

                user_by_phone.registered = True
                user_by_phone.set_password(password)
                user_by_phone.save()
                token_old_or_new, token_old_or_new_created = Token.objects.get_or_create(user=user_by_phone)

                return Response({
                    'success': True,
                    'detail': 'Успешно зашли и зарегестрировали пользователя',
                    'token': token_old_or_new.key,
                }, status=200)
            
        else:
            return Response({
                'success': False,
                'detail': 'Вы не предоставили данные'
            }, status=400)


class UserDetailView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def retrieve(self, request, pk=None):
        query = User.objects.all()
        user = generics.get_object_or_404(query, id=request.user.id)
        player_id = self.request.query_params.get('player_id')
        if player_id:
            user.player_id = player_id
        currentTime = datetime.now()
        user.last_login = currentTime
        user.save()
        serializer = UserDetaiSerializer(user)
        return Response(serializer.data)

class DeletePlayerID(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, *args, **kwargs):
        request.user.player_id = None
        request.user.save()
        return Response({
            'success': True,
            'detail': 'Успешно удалили'
        }, 
        status=200)









# APP 
class PackagesListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PackageDetailSerializer
    pagination_class = PaginationAll
    def get_queryset(self):
        return Package.objects.filter(user=self.request.user).filter(Q(status='added') | Q(status='sent')).order_by('-id')


class MyReceiptsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PackageDetailSerializer
    pagination_class = PaginationPackages
    def get_queryset(self):
        return Package.objects.filter(user=self.request.user).filter(Q(status='given') | Q(status='arrived')).order_by('-id')

class CreatePackage(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        track_code = request.data.get('track_code')
        if track_code:
            new_package = Package()
            new_package.user = request.user
            new_package.track_code = track_code
            new_package.save()
            return Response({
                'success': True,
                'detail': 'Успешно создали трек',
            }, status=200)
        else:
            return Response({
                'success': False,
                'detail': 'Вы не предоставили данные'
            }, status=400)




class NotificationsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationDetailSerializer
    pagination_class = PaginationAll
    def get_queryset(self):
        all_notifications = Notification.objects.all().order_by('-id')
        new_notifications = []
        all_showed_notifications = UserShowedNotification.objects.filter(user=self.request.user)
        all_showed_notifications_ids = []

        for showed in all_showed_notifications:
            all_showed_notifications_ids.append(showed.notification.id)

        for notification in all_notifications:
            if (notification.id in all_showed_notifications_ids) == False:
                if notification.disappears:
                    new_showed = UserShowedNotification()
                    new_showed.notification = notification
                    new_showed.user = self.request.user
                    new_showed.save()
                new_notifications.append(notification)
        return new_notifications






#Caravan Manager
class GetStatistics(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        custom_token = request.data.get('custom_token')
        if custom_token == ConstantsCustom.custom_token:
            users = User.objects.all().count()
            packages = Package.objects.filter(user=self.request.user).filter(Q(status='added') | Q(status='sent')).count()
            receipts = Package.objects.filter(user=self.request.user).filter(Q(status='given') | Q(status='arrived')).count()
            
            return Response({
                'success': True,
                'users': users-1,
                'packages': packages,
                'receipts': receipts,
                'detail': 'Успешно получили статистику',
            }, status=200)
        else:
            return Response({
                'success': False,
                'detail': 'Вы не предоставили данные'
            }, status=400)




class SearchPackagesListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PackageDetailSerializer
    pagination_class = PaginationPackages
    def get_queryset(self):
        search_text = self.request.GET.get('search_text', None)
        if search_text == None:
            return []
        return Package.objects.filter(track_code__icontains=search_text).order_by('-id')



class UpdatePackageView(generics.UpdateAPIView):
    serializer_class = PackageDetailSerializer
    queryset = Package.objects.all()
    def perform_update(self, serializer):
        package = Package.objects.filter(id=self.kwargs['pk']).first()
        if package.status != serializer.validated_data['status'] and package.user.player_id:
            print('push sent')
            PushHelper.sendPushNotifications(ids=[package.user.player_id], subject='Посылка: {}'.format(package.track_code), content=convertStatusToText(serializer.validated_data['status']))
        serializer.save()

def convertStatusToText(status):
    if status == 'added':
        return 'Статус посылки добавлено!'
    if status == 'sent':
        return 'Статус посылки отправлено!'
    if status == 'arrived':
        return 'Статус посылки прибыло!'
    if status == 'given':
        return 'Статус посылки выдано!'


class CreateNotification(APIView):
    def post(self, request, *args, **kwargs):
        custom_token = request.data.get('custom_token')
        title = request.data.get('title')
        description = request.data.get('description')
        disappears = request.data.get('disappears')
        if title and (disappears is not None) and custom_token == ConstantsCustom.custom_token:
            new_notifcation = Notification()        

            if description:
                new_notifcation.description = description
            
            new_notifcation.title = title
            new_notifcation.disappears = disappears
            new_notifcation.save()


            #ОТПРАВКА ПУША ЧЕРЕЗ ONESIGNAL
            res = None
            users = User.objects.all().exclude(player_id__isnull=True)
            lastUser = users.last()
            device_ids = []
            limit = 2000
            id_count = 0
            for user in users:
                if lastUser.id == user.id:
                    res = PushHelper.sendPushNotifications(ids=device_ids, subject=title, content=description)
                elif id_count == (limit-1) and user.player_id is not None:
                    res = PushHelper.sendPushNotifications(ids=device_ids, subject=title, content=description)
                    id_count = 0
                    device_ids = []
                    id_count = id_count+1
                    device_ids.append(user.player_id)
                elif user.player_id is not None:
                    id_count = id_count+1
                    device_ids.append(user.player_id)
            #....


            return Response({
                'success': True,
                'detail': 'Успешно создали уведомление!',
            }, status=200)
        else:
            return Response({
                'success': False,
                'detail': 'Вы не предоставили данные'
            }, status=400)