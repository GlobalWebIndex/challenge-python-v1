from django.contrib.auth.models import User, Group, Permission
from django.test import TestCase
from django.urls import reverse

from dinosaurs.models import Dinosaur


class DinosaurListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for dinosaur_id in range(16):
            Dinosaur.objects.create(name=f'T-Rex {dinosaur_id}')

    def test_view_url_exists(self):
        response = self.client.get('/dinosaurs/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get((reverse('dinosaur')))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get((reverse('dinosaur')))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name='dinosaurs/dinosaur_list.html')

    def test_pagination_is_twelve(self):
        response = self.client.get((reverse('dinosaur')))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['dinosaur_list']), 12)

    def test_list_all_dinosaurs(self):
        response = self.client.get(reverse('dinosaur') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['dinosaur_list']), 4)


class DinosaurDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Dinosaur.objects.create(name='T-Rex')

    def test_view_url_exists(self):
        response = self.client.get('/dinosaurs/dinosaur/1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get((reverse('dinosaur-detail', args='1')))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get((reverse('dinosaur-detail', args='1')))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name='dinosaurs/dinosaur_detail.html')


class SearchResultsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Dinosaur.objects.create(name='test-name')
        for dinosaur_id in range(10):
            Dinosaur.objects.create(name=f'T-REX {dinosaur_id}')

    def test_view_url_exists(self):
        response = self.client.get('/dinosaurs/search/?q=')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/dinosaurs/search/?q=T-Rex')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response=response, template_name='dinosaurs/search_results.html')

    def test_view_when_results_are_found(self):
        response = self.client.get('/dinosaurs/search/?q=rex')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['dinosaur_list']), 10)

    def test_view_when_no_result_found(self):
        response = self.client.get('/dinosaurs/search/?q=no-result-should-be-found')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['dinosaur_list']), 0)


class DinosaurCreateViewTest(TestCase):
    @classmethod
    def setUp(cls):
        administrator_group = Group.objects.create(name='Administrator Members')
        administrator_group.save()
        developer_group = Group.objects.create(name='Developer Members')
        developer_group.save()

        admin_user = User.objects.create_user(username='admin_user', password='password1')
        admin_user.save()
        admin_user.groups.add(administrator_group)
        admin_user.user_permissions.add((Permission.objects.get(codename='can_edit')))
        developer_user = User.objects.create_user(username='developer_user', password='password2')
        developer_user.save()

        for dinosaur_id in range(10):
            Dinosaur.objects.create(name=f'T-REX {dinosaur_id}')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('dinosaur-create'))
        self.assertRedirects(response, '/accounts/login/?next=/dinosaurs/create/')

    def test_logged_in_admin_user_with_edit_permission_correct_template(self):
        login = self.client.login(username='admin_user', password='password1')
        response = self.client.get(reverse('dinosaur-create'))
        self.assertEqual(str(response.context['user']), 'admin_user')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dinosaurs/dinosaur_form.html')

    def test_logged_in_developer_user_without_edit_permission_forbidden(self):
        login = self.client.login(username='developer_user', password='password2')
        response = self.client.get(reverse('dinosaur-create'))
        self.assertEqual(response.status_code, 403)


class DinosaurUpdateViewTest(TestCase):
    @classmethod
    def setUp(cls):
        administrator_group = Group.objects.create(name='Administrator Members')
        administrator_group.save()
        developer_group = Group.objects.create(name='Developer Members')
        developer_group.save()

        admin_user = User.objects.create_user(username='admin_user', password='password1')
        admin_user.save()
        admin_user.groups.add(administrator_group)
        admin_user.user_permissions.add((Permission.objects.get(codename='can_edit')))
        developer_user = User.objects.create_user(username='developer_user', password='password2')
        developer_user.save()

        for dinosaur_id in range(10):
            Dinosaur.objects.create(name=f'T-REX {dinosaur_id}')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('dinosaur-update', args='1'))
        self.assertRedirects(response, '/accounts/login/?next=/dinosaurs/update/1/')

    def test_logged_in_admin_user_with_edit_permission_correct_template(self):
        login = self.client.login(username='admin_user', password='password1')
        response = self.client.get(reverse('dinosaur-update', args='1'))
        self.assertEqual(str(response.context['user']), 'admin_user')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dinosaurs/dinosaur_form_update.html')

    def test_logged_in_developer_user_without_edit_permission_forbidden(self):
        login = self.client.login(username='developer_user', password='password2')
        response = self.client.get(reverse('dinosaur-update', args='1'))
        self.assertEqual(response.status_code, 403)

    def test_when_update_non_existing_dinosaur_returns_404(self):
        login = self.client.login(username='admin_user', password='password1')
        response = self.client.get(reverse('dinosaur-update', args=(123,)))
        self.assertEqual(response.status_code, 404)


class DinosaurDeleteViewTest(TestCase):
    @classmethod
    def setUp(cls):
        administrator_group = Group.objects.create(name='Administrator Members')
        administrator_group.save()
        developer_group = Group.objects.create(name='Developer Members')
        developer_group.save()

        admin_user = User.objects.create_user(username='admin_user', password='password1')
        admin_user.save()
        admin_user.groups.add(administrator_group)
        admin_user.user_permissions.add((Permission.objects.get(codename='can_edit')))
        developer_user = User.objects.create_user(username='developer_user', password='password2')
        developer_user.save()

        for dinosaur_id in range(10):
            Dinosaur.objects.create(name=f'T-REX {dinosaur_id}')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('dinosaur-delete', args='1'))
        self.assertRedirects(response, '/accounts/login/?next=/dinosaurs/delete/1/')

    def test_logged_in_admin_user_with_edit_permission_correct_template(self):
        login = self.client.login(username='admin_user', password='password1')
        response = self.client.get(reverse('dinosaur-delete', args='1'))
        self.assertEqual(str(response.context['user']), 'admin_user')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dinosaurs/dinosaur_confirm_delete.html')

    def test_logged_in_developer_user_without_edit_permission_forbidden(self):
        login = self.client.login(username='developer_user', password='password2')
        response = self.client.get(reverse('dinosaur-delete', args='1'))
        self.assertEqual(response.status_code, 403)

    def test_when_delete_non_existing_dinosaur_returns_404(self):
        login = self.client.login(username='admin_user', password='password1')
        response = self.client.get(reverse('dinosaur-delete', args=(123,)))
        self.assertEqual(response.status_code, 404)
