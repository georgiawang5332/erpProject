# Generated by Django 4.2.7 on 2024-09-03 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='部門名稱')),
            ],
            options={
                'verbose_name': '部門名稱',
                'verbose_name_plural': '部門名稱',
            },
        ),
        migrations.CreateModel(
            name='EducationLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(max_length=100, unique=True, verbose_name='教育程度')),
            ],
            options={
                'verbose_name': '教育程度',
                'verbose_name_plural': '教育程度',
            },
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=255, null=True, unique=True)),
                ('subject', models.CharField(max_length=200, verbose_name='主題')),
                ('message', models.TextField(verbose_name='留言訊息')),
                ('from_email', models.EmailField(max_length=254, verbose_name='來自郵件')),
                ('to_email', models.EmailField(max_length=254, verbose_name='收件者郵件帳號')),
                ('received_at', models.DateTimeField(blank=True, null=True, verbose_name='接收時間')),
                ('is_sent', models.BooleanField(default=False, verbose_name='是否已發送')),
                ('folder', models.CharField(max_length=50, verbose_name='資料夾')),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '郵件',
                'verbose_name_plural': '郵件',
            },
        ),
        migrations.CreateModel(
            name='EmploymentCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=50, unique=True, verbose_name='聘僱類別')),
            ],
            options={
                'verbose_name': '聘僱類別',
                'verbose_name_plural': '聘僱類別',
            },
        ),
        migrations.CreateModel(
            name='EmploymentStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=20, unique=True, verbose_name='狀態')),
                ('description', models.TextField(blank=True, verbose_name='描述')),
            ],
            options={
                'verbose_name': '在職狀態',
                'verbose_name_plural': '在職狀態',
            },
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='性別')),
            ],
            options={
                'verbose_name': '性別',
                'verbose_name_plural': '性別',
            },
        ),
        migrations.CreateModel(
            name='MaritalStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50, unique=True, verbose_name='婚姻狀態')),
            ],
            options={
                'verbose_name': '婚姻狀態',
                'verbose_name_plural': '婚姻狀態',
            },
        ),
        migrations.CreateModel(
            name='RecruitmentSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=50, unique=True, verbose_name='招聘來源')),
            ],
            options={
                'verbose_name': '招聘來源',
                'verbose_name_plural': '招聘來源',
            },
        ),
        migrations.CreateModel(
            name='SendEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200, verbose_name='主題')),
                ('message', models.TextField(verbose_name='留言訊息')),
                ('from_email', models.EmailField(default='georgiawang5332@gmail.com', editable=False, max_length=254, verbose_name='(從)來自郵件')),
                ('to_email', models.EmailField(max_length=254, verbose_name='(到)收件者郵件帳號')),
            ],
            options={
                'verbose_name': '寄發郵件',
                'verbose_name_plural': '寄發郵件',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataNum', models.CharField(max_length=30, unique=True, verbose_name='資料編號')),
                ('name', models.CharField(max_length=100, verbose_name='姓名')),
                ('engName', models.CharField(max_length=100, verbose_name='英文名')),
                ('ID_Card', models.CharField(max_length=100, verbose_name='身分證字號')),
                ('dateOfBirth', models.DateField(verbose_name='出生日期')),
                ('jobNum', models.CharField(max_length=4, unique=True, verbose_name='工號')),
                ('employeeAccount', models.CharField(max_length=50, unique=True, verbose_name='員工帳號')),
                ('jobTitle', models.CharField(max_length=50, verbose_name='職稱')),
                ('grade', models.CharField(max_length=50, verbose_name='職等')),
                ('companyPhone', models.CharField(max_length=50, verbose_name='公司電話')),
                ('extension', models.CharField(max_length=50, verbose_name='分機')),
                ('companyMobilePhone', models.CharField(max_length=50, verbose_name='公司手機')),
                ('companyMailbox', models.CharField(max_length=50, verbose_name='公司信箱')),
                ('startDate', models.DateField(max_length=50, verbose_name='到職日期')),
                ('resignationDate', models.DateField(blank=True, max_length=50, null=True, verbose_name='離職日期')),
                ('remark', models.TextField(max_length=50, verbose_name='備註')),
                ('OTJStatus', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='PersonnelAddressBook.employmentstatus', verbose_name='在職狀態')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='PersonnelAddressBook.department', verbose_name='部門')),
                ('empCategory', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='PersonnelAddressBook.employmentcategory', verbose_name='聘僱類別')),
                ('gender', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='PersonnelAddressBook.gender', verbose_name='性別')),
                ('highestEduLev', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='PersonnelAddressBook.educationlevel', verbose_name='最高教育程度')),
                ('immediateSupervisor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='PersonnelAddressBook.employee', verbose_name='直屬主管')),
                ('maritalStatus', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='PersonnelAddressBook.maritalstatus', verbose_name='婚姻狀態')),
                ('recruitmentSource', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='PersonnelAddressBook.recruitmentsource', verbose_name='招聘來源')),
            ],
            options={
                'verbose_name': '員工資料',
                'verbose_name_plural': '員工資料',
            },
        ),
        migrations.CreateModel(
            name='GroupEmail',
            fields=[
                ('number', models.AutoField(primary_key=True, serialize=False)),
                ('action', models.CharField(default='加入', max_length=50)),
                ('is_read', models.BooleanField(default=False)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_emails', to='PersonnelAddressBook.employee')),
            ],
            options={
                'verbose_name': '群組郵件',
                'verbose_name_plural': '群組郵件',
                'ordering': ['-number'],
                'unique_together': {('employee',)},
            },
        ),
    ]
