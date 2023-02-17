from django.urls import path
from .views import *



urlpatterns = [
    #Auth
        # Authorization
        path('login-client/', LoginUser.as_view()),
        path('create-client/', CreateUser.as_view()),
        path('get-user-info/', UserDetailView.as_view({'get': 'retrieve'})),
        
        path('delete-player-id/', DeletePlayerID.as_view()),

    path('get-packages/', PackagesListView.as_view()),
    path('get-receipts/', MyReceiptsListView.as_view()),
    path('create-package/', CreatePackage.as_view()),

    path('get-notifications/', NotificationsListView.as_view()),
    path('get-stats/', GetStatistics.as_view()),
    path('get-by-search-packages/', SearchPackagesListView.as_view()),
    path('update-package/<int:pk>/', UpdatePackageView.as_view()),
    path('create-notification/', CreateNotification.as_view()),

]