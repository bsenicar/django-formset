from django.forms import fields, widgets
from django.forms.models import ModelForm, construct_instance, model_to_dict

from formset.collection import FormCollection
from formset.renderers.bootstrap import FormRenderer

from testapp.models import Company, Member, Team


class CompanyForm(ModelForm):
    id = fields.IntegerField(
        required=False,
        widget=widgets.HiddenInput,
    )

    class Meta:
        model = Company
        fields = '__all__'


class TeamForm(ModelForm):
    id = fields.IntegerField(
        required=False,
        widget=widgets.HiddenInput,
    )

    class Meta:
        model = Team
        fields = ['id', 'name']


class MemberForm(ModelForm):
    id = fields.IntegerField(
        required=False,
        widget=widgets.HiddenInput,
    )

    class Meta:
        model = Member
        fields = ['id', 'name']


class MemberCollection(FormCollection):
    min_siblings = 0
    member = MemberForm()
    add_label = "Add Member"

    def model_to_dict(self, team):
        fields = self.declared_holders['member']._meta.fields
        return [{'member': model_to_dict(member, fields=fields)}
                for member in team.members.all()]

    def retrieve_instance(self, data):
        if data := data.get('member'):
            try:
                return self.instance.members.get(id=data.get('id') or 0)
            except Member.DoesNotExist:
                return Member(name=data.get('name'), team=self.instance)

    def construct_instance(self, team):
        for holder in self.valid_holders:
            member_form = holder['member']
            instance = member_form.instance
            if member_form.marked_for_removal:
                instance.delete()
                continue
            construct_instance(member_form, instance)
            member_form.save()


class TeamCollection(FormCollection):
    min_siblings = 0
    team = TeamForm()
    members = MemberCollection()
    legend = "Team"
    add_label = "Add Team"

    def model_to_dict(self, company):
        fields = self.declared_holders['team']._meta.fields
        data = []
        for team in company.teams.all():
            data.append({
                'team': model_to_dict(team, fields=fields),
                'members': self.declared_holders['members'].model_to_dict(team),
            })
        return data

    def retrieve_instance(self, data):
        if data := data.get('team'):
            try:
                return self.instance.teams.get(id=data.get('id') or 0)
            except Team.DoesNotExist:
                return Team(name=data.get('name'), company=self.instance)

    def construct_instance(self, company):
        for holder in self.valid_holders:
            team_form = holder['team']
            instance = team_form.instance
            if team_form.marked_for_removal:
                instance.delete()
                continue
            construct_instance(team_form, instance)
            team_form.save()
            holder['members'].construct_instance(instance)


class GumishCollection(FormCollection):
    default_renderer = FormRenderer(collection_css_classes='col card p-3')

    company = CompanyForm()
    teams = TeamCollection()
