"""
URL configuration for erpProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # 業務項目很多種
    path("sendEmail/", include("sendEmail.urls")),
    path("PersonnelAddressBook/", include("PersonnelAddressBook.urls")),
    path("Resume/", include("Resume.urls")),

    path("BudgetSheet/", include("BudgetSheet.urls")),
    path("PreparationFlowChart/", include("PreparationFlowChart.urls")),
    path("InviteSendForm/", include("InviteSendForm.urls")),
    path("CeremonyWeddingChecklist/", include("CeremonyWeddingChecklist.urls")),
    path("DayItemList/", include("DayItemList.urls")),
    path("DayProcess/", include("DayProcess.urls")),
    path("CarAllocation/", include("CarAllocation.urls")),
    path("BanquetStaffList/", include("BanquetStaffList.urls")),
    path("SeatingAssignments/", include("SeatingAssignments.urls")),
    
    # 基本項目
    path("invitationCard/", include("invitationCard.urls")),
    path("calendarapp/", include("calendarapp.urls")),
    path('accounts/', include('accounts.urls', namespace='accounts')),

    path("dashboard/", include("dashboard.urls")),
    path("", include("website.urls")),    
    
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)