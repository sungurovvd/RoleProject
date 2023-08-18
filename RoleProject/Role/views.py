from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm
from .models import *
from django.views.generic import View,CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse


class UserList(LoginRequiredMixin, ListView):
    model = User
    context_object_name = 'users'
    paginate_by = 10
    template_name = 'all_users.html'


class RoleList(LoginRequiredMixin, ListView):
    model = Role
    context_object_name = 'roles'
    paginate_by = 10
    template_name = 'all_roles.html'


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login')


class CreateRole(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        rights = Right.objects.all()
        servers = Server.objects.all()
        to_html = {'right': rights,
                   'server': servers}
        return render(request, 'create_role.html', context=to_html)

    def post(self, request, *args, **kwargs):
        checked = request.POST.getlist('checkbox')
        created_user = request.POST['user']
        user_from = User.objects.get(username=f'{created_user}')
        role_name = request.POST['header']

        new_role = Role(
            name=role_name,
            status_id = Status.objects.get(id=4),
            create_user = user_from ,
            approve_user = User.objects.get(id=1)
        )
        new_role.save()

        for r in checked:
            right_from_list = Right.objects.get(id=int(r))
            right_from_list.role.add(new_role)

        servers = request.POST.getlist('server')
        for s in servers:
            allowed_server = ServersForRole(
                server_id = Server.objects.get(id=int(s)),
                role_id = new_role
            )
            allowed_server.save()

        return redirect('roles')


class ChangeStatus(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        aut_user = request.user.username
        usr = User.objects.get(username=f'{aut_user}')
        usrrl = UserRole.objects.filter(user_id = usr)
        for role in usrrl:
            if role.role_id.status_id.status == 'Confirmed':
                rights = role.role_id.right_set.all()
                for right in rights:
                    if right.name == 'approve roles':
                        id = 0
                        for pk, number in kwargs.items():
                            id = int(number)

                        rl = Role.objects.get(id=id)
                        role_rights = Right.objects.filter(role=rl)
                        stts = Status.objects.all()
                        serversforrole = ServersForRole.objects.filter(role_id = rl)

                        to_html = { 'role_name': rl.name,
                                    'rights': role_rights,
                                    'status': stts,
                                    'allowed_servers': serversforrole
                        }
                        return render(request, 'change_status.html', context=to_html)
        return render(request, 'you_havnt_rights.html')

    def post(self, request, *args, **kwargs):
        id = 0
        for pk, number in kwargs.items():
            id = int(number)
        new_status = Status.objects.get(id = request.POST['status_list'])
        created_user = request.user.username
        rl = Role.objects.get(id=id)
        print(request.POST['status_list'])
        if new_status == Status.objects.get(id=3):
            print('in if')
            on_del = UserRole.objects.filter(role_id=rl)
            print(on_del)
            for d in on_del:
                print(d)
                d.delete()
        rl.status_id = new_status
        rl.approve_user = User.objects.get(username=f'{created_user}')
        rl.save()
        return redirect('roles')


class AddRoleToUser(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):

        aut_user = request.user.username
        usr = User.objects.get(username=f'{aut_user}')
        usrrl = UserRole.objects.filter(user_id = usr)
        for role in usrrl:
            if role.role_id.status_id.status == 'Confirmed':
                rights = role.role_id.right_set.all()
                for right in rights:
                    if right.name == 'approve roles':
                        id = 0
                        for pk, number in kwargs.items():
                            id = int(number)

                        usr = User.objects.get(id=id)
                        servers = Server.objects.all().order_by('id')
                        server_role = ServersForRole.objects.all().order_by('server_id')
                        usr_role = UserRole.objects.filter(user_id = usr).order_by('server_id')
                        dict_server_roles = {}
                        for server in servers:
                            dict_server_roles[server.server_name] = []
                        for smt in usr_role:
                            if smt.role_id.status_id.status == "Confirmed":
                                dict_server_roles[smt.server_id.server_name].append(smt.role_id.name)

                        to_html = { 'usr': usr,
                                    'server_role': server_role,
                                    'servers': servers,
                                    'dict': dict_server_roles
                        }
                        return render(request, 'add_role_to_user.html', context=to_html)
        return render(request, 'you_havnt_rights.html')

    def post(self, request, *args, **kwargs):
        id = 0
        for pk, number in kwargs.items():
            id = int(number)
        usr = User.objects.get(id=id)
        servers = Server.objects.all().order_by('id')
        for server in servers:
            checked = request.POST.getlist(f'{server.id}')
            int_checked = [int(item) for item in checked]
            usr_rl = UserRole.objects.filter(user_id=usr, server_id = server)
            usr_rl_id = [item.role_id.id for item in usr_rl]
            difference = set(usr_rl_id) ^ set(int_checked)


            for role in difference:
                #если раньше нужно удалить юзерроль
                rl = Role.objects.get(id=role)
                if role in usr_rl_id:
                    on_del = UserRole.objects.get(user_id = usr, role_id = rl, server_id = server)
                    on_del.delete()
                else:
                    #если нужно создать
                    new_usr_rl = UserRole(
                        user_id = usr,
                        role_id = rl,
                        server_id = server,
                    )
                    new_usr_rl.save()

        return redirect('user')

class CreateRole(LoginRequiredMixin, View):
    def post(self):
        


