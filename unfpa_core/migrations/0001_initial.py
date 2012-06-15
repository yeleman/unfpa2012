# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'MaternalMortalityReport'
        db.create_table('unfpa_core_maternalmortalityreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='unfpa_core_maternalmortalityreport_reports', to=orm['bolibana.Provider'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolibana.Provider'], null=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('reporting_location', self.gf('django.db.models.fields.related.ForeignKey')(related_name='maternal_reported_in', to=orm['bolibana.Entity'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('dob', self.gf('django.db.models.fields.DateField')()),
            ('dob_auto', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('dod', self.gf('django.db.models.fields.DateField')()),
            ('death_location', self.gf('django.db.models.fields.related.ForeignKey')(related_name='maternal_dead_in', to=orm['bolibana.Entity'])),
            ('living_children', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('dead_children', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pregnant', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pregnancy_weeks', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('pregnancy_related_death', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('unfpa_core', ['MaternalMortalityReport'])

        # Adding model 'ChildrenMortalityReport'
        db.create_table('unfpa_core_childrenmortalityreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='unfpa_core_childrenmortalityreport_reports', to=orm['bolibana.Provider'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolibana.Provider'], null=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('reporting_location', self.gf('django.db.models.fields.related.ForeignKey')(related_name='children_reported_in', to=orm['bolibana.Entity'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('sex', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('dob', self.gf('django.db.models.fields.DateField')()),
            ('dob_auto', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('dod', self.gf('django.db.models.fields.DateField')()),
            ('death_location', self.gf('django.db.models.fields.related.ForeignKey')(related_name='children_dead_in', to=orm['bolibana.Entity'])),
            ('death_place', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('unfpa_core', ['ChildrenMortalityReport'])

        # Adding model 'RHCommoditiesReport'
        db.create_table('unfpa_core_rhcommoditiesreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_status', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('type', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('receipt', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30, blank=True)),
            ('period', self.gf('django.db.models.fields.related.ForeignKey')(related_name='unfpa_core_rhcommoditiesreport_reports', to=orm['bolibana.Period'])),
            ('entity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='unfpa_core_rhcommoditiesreport_reports', to=orm['bolibana.Entity'])),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='unfpa_core_rhcommoditiesreport_reports', to=orm['bolibana.Provider'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolibana.Provider'], null=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('family_planning', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('delivery_services', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('male_condom', self.gf('django.db.models.fields.IntegerField')()),
            ('female_condom', self.gf('django.db.models.fields.IntegerField')()),
            ('oral_pills', self.gf('django.db.models.fields.IntegerField')()),
            ('injectable', self.gf('django.db.models.fields.IntegerField')()),
            ('iud', self.gf('django.db.models.fields.IntegerField')()),
            ('implants', self.gf('django.db.models.fields.IntegerField')()),
            ('female_sterilization', self.gf('django.db.models.fields.IntegerField')()),
            ('male_sterilization', self.gf('django.db.models.fields.IntegerField')()),
            ('amoxicillin_ij', self.gf('django.db.models.fields.IntegerField')()),
            ('amoxicillin_cap_gel', self.gf('django.db.models.fields.IntegerField')()),
            ('amoxicillin_suspension', self.gf('django.db.models.fields.IntegerField')()),
            ('azithromycine_tab', self.gf('django.db.models.fields.IntegerField')()),
            ('azithromycine_suspension', self.gf('django.db.models.fields.IntegerField')()),
            ('benzathine_penicillin', self.gf('django.db.models.fields.IntegerField')()),
            ('cefexime', self.gf('django.db.models.fields.IntegerField')()),
            ('clotrimazole', self.gf('django.db.models.fields.IntegerField')()),
            ('ergometrine_tab', self.gf('django.db.models.fields.IntegerField')()),
            ('ergometrine_vials', self.gf('django.db.models.fields.IntegerField')()),
            ('iron', self.gf('django.db.models.fields.IntegerField')()),
            ('folate', self.gf('django.db.models.fields.IntegerField')()),
            ('iron_folate', self.gf('django.db.models.fields.IntegerField')()),
            ('magnesium_sulfate', self.gf('django.db.models.fields.IntegerField')()),
            ('metronidazole', self.gf('django.db.models.fields.IntegerField')()),
            ('oxytocine', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('unfpa_core', ['RHCommoditiesReport'])

        # Adding unique constraint on 'RHCommoditiesReport', fields ['period', 'entity', 'type']
        db.create_unique('unfpa_core_rhcommoditiesreport', ['period_id', 'entity_id', 'type'])

        # Adding M2M table for field sources on 'RHCommoditiesReport'
        db.create_table('unfpa_core_rhcommoditiesreport_sources', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_rhcommoditiesreport', models.ForeignKey(orm['unfpa_core.rhcommoditiesreport'], null=False)),
            ('to_rhcommoditiesreport', models.ForeignKey(orm['unfpa_core.rhcommoditiesreport'], null=False))
        ))
        db.create_unique('unfpa_core_rhcommoditiesreport_sources', ['from_rhcommoditiesreport_id', 'to_rhcommoditiesreport_id'])

        # Adding model 'ProvidedServicesReport'
        db.create_table('unfpa_core_providedservicesreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('_status', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('type', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('receipt', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30, blank=True)),
            ('period', self.gf('django.db.models.fields.related.ForeignKey')(related_name='unfpa_core_providedservicesreport_reports', to=orm['bolibana.Period'])),
            ('entity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='unfpa_core_providedservicesreport_reports', to=orm['bolibana.Entity'])),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='unfpa_core_providedservicesreport_reports', to=orm['bolibana.Provider'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolibana.Provider'], null=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('iud', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('injectable', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('oral_pills', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('male_condom', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('female_condom', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('emergency_contraception', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('implant', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('new_client', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('returning_client', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pf_visit_u25', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pf_visit_o25', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pf_first_time', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pf_visit_ams_ticket', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pf_visit_provider_ticket', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pf_visit_short_term', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pf_visit_long_term', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('client_hiv_counselling', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('client_hiv_tested', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('client_hiv_positive', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('implant_removal', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('iud_removal', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('total_hiv_test', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('unfpa_core', ['ProvidedServicesReport'])

        # Adding unique constraint on 'ProvidedServicesReport', fields ['period', 'entity', 'type']
        db.create_unique('unfpa_core_providedservicesreport', ['period_id', 'entity_id', 'type'])

        # Adding M2M table for field sources on 'ProvidedServicesReport'
        db.create_table('unfpa_core_providedservicesreport_sources', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_providedservicesreport', models.ForeignKey(orm['unfpa_core.providedservicesreport'], null=False)),
            ('to_providedservicesreport', models.ForeignKey(orm['unfpa_core.providedservicesreport'], null=False))
        ))
        db.create_unique('unfpa_core_providedservicesreport_sources', ['from_providedservicesreport_id', 'to_providedservicesreport_id'])

        # Adding model 'BirthReport'
        db.create_table('unfpa_core_birthreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='unfpa_core_birthreport_reports', to=orm['bolibana.Provider'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolibana.Provider'], null=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('reporting_location', self.gf('django.db.models.fields.related.ForeignKey')(related_name='birth_reported_in', to=orm['bolibana.Entity'])),
            ('family_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('surname_mother', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('surname_child', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('sex', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('dob', self.gf('django.db.models.fields.DateField')()),
            ('dob_auto', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('born_alive', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('birth_location', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('unfpa_core', ['BirthReport'])

        # Adding model 'PregnancyReport'
        db.create_table('unfpa_core_pregnancyreport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='unfpa_core_pregnancyreport_reports', to=orm['bolibana.Provider'])),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bolibana.Provider'], null=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('reporting_location', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pregnancy_reported_in', to=orm['bolibana.Entity'])),
            ('householder_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('mother_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('dob', self.gf('django.db.models.fields.DateField')()),
            ('dob_auto', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pregnancy_age', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('expected_delivery_date', self.gf('django.db.models.fields.DateField')()),
            ('delivery_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('pregnancy_result', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
        ))
        db.send_create_signal('unfpa_core', ['PregnancyReport'])

        # Adding model 'UEntity'
        db.create_table('unfpa_core_uentity', (
            ('entity_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bolibana.Entity'], unique=True, primary_key=True)),
            ('is_unfpa', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_credos', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('unfpa_core', ['UEntity'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'ProvidedServicesReport', fields ['period', 'entity', 'type']
        db.delete_unique('unfpa_core_providedservicesreport', ['period_id', 'entity_id', 'type'])

        # Removing unique constraint on 'RHCommoditiesReport', fields ['period', 'entity', 'type']
        db.delete_unique('unfpa_core_rhcommoditiesreport', ['period_id', 'entity_id', 'type'])

        # Deleting model 'MaternalMortalityReport'
        db.delete_table('unfpa_core_maternalmortalityreport')

        # Deleting model 'ChildrenMortalityReport'
        db.delete_table('unfpa_core_childrenmortalityreport')

        # Deleting model 'RHCommoditiesReport'
        db.delete_table('unfpa_core_rhcommoditiesreport')

        # Removing M2M table for field sources on 'RHCommoditiesReport'
        db.delete_table('unfpa_core_rhcommoditiesreport_sources')

        # Deleting model 'ProvidedServicesReport'
        db.delete_table('unfpa_core_providedservicesreport')

        # Removing M2M table for field sources on 'ProvidedServicesReport'
        db.delete_table('unfpa_core_providedservicesreport_sources')

        # Deleting model 'BirthReport'
        db.delete_table('unfpa_core_birthreport')

        # Deleting model 'PregnancyReport'
        db.delete_table('unfpa_core_pregnancyreport')

        # Deleting model 'UEntity'
        db.delete_table('unfpa_core_uentity')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'bolibana.access': {
            'Meta': {'unique_together': "(('role', 'content_type', 'object_id'),)", 'object_name': 'Access'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolibana.Role']"})
        },
        'bolibana.entity': {
            'Meta': {'object_name': 'Entity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['bolibana.Entity']"}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '12', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '15', 'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entities'", 'to': "orm['bolibana.EntityType']"})
        },
        'bolibana.entitytype': {
            'Meta': {'object_name': 'EntityType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '15', 'db_index': 'True'})
        },
        'bolibana.period': {
            'Meta': {'unique_together': "(('start_on', 'end_on', 'period_type'),)", 'object_name': 'Period'},
            'end_on': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'period_type': ('django.db.models.fields.CharField', [], {'default': "'custom'", 'max_length': '15'}),
            'start_on': ('django.db.models.fields.DateTimeField', [], {})
        },
        'bolibana.permission': {
            'Meta': {'object_name': 'Permission'},
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'primary_key': 'True', 'db_index': 'True'})
        },
        'bolibana.provider': {
            'Meta': {'object_name': 'Provider'},
            'access': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['bolibana.Access']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '12', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'phone_number_extra': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'pwhash': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'bolibana.role': {
            'Meta': {'object_name': 'Role'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['bolibana.Permission']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '15', 'primary_key': 'True', 'db_index': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'unfpa_core.birthreport': {
            'Meta': {'object_name': 'BirthReport'},
            'birth_location': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'born_alive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'unfpa_core_birthreport_reports'", 'to': "orm['bolibana.Provider']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {}),
            'dob_auto': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'family_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolibana.Provider']", 'null': 'True', 'blank': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'reporting_location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'birth_reported_in'", 'to': "orm['bolibana.Entity']"}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'surname_child': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'surname_mother': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'unfpa_core.childrenmortalityreport': {
            'Meta': {'object_name': 'ChildrenMortalityReport'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'unfpa_core_childrenmortalityreport_reports'", 'to': "orm['bolibana.Provider']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'death_location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children_dead_in'", 'to': "orm['bolibana.Entity']"}),
            'death_place': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'dob': ('django.db.models.fields.DateField', [], {}),
            'dob_auto': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dod': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolibana.Provider']", 'null': 'True', 'blank': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'reporting_location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children_reported_in'", 'to': "orm['bolibana.Entity']"}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'unfpa_core.maternalmortalityreport': {
            'Meta': {'object_name': 'MaternalMortalityReport'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'unfpa_core_maternalmortalityreport_reports'", 'to': "orm['bolibana.Provider']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dead_children': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'death_location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'maternal_dead_in'", 'to': "orm['bolibana.Entity']"}),
            'dob': ('django.db.models.fields.DateField', [], {}),
            'dob_auto': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dod': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'living_children': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolibana.Provider']", 'null': 'True', 'blank': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pregnancy_related_death': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pregnancy_weeks': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pregnant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reporting_location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'maternal_reported_in'", 'to': "orm['bolibana.Entity']"})
        },
        'unfpa_core.pregnancyreport': {
            'Meta': {'object_name': 'PregnancyReport'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'unfpa_core_pregnancyreport_reports'", 'to': "orm['bolibana.Provider']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'delivery_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {}),
            'dob_auto': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'expected_delivery_date': ('django.db.models.fields.DateField', [], {}),
            'householder_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolibana.Provider']", 'null': 'True', 'blank': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'mother_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pregnancy_age': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'pregnancy_result': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'reporting_location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pregnancy_reported_in'", 'to': "orm['bolibana.Entity']"})
        },
        'unfpa_core.providedservicesreport': {
            'Meta': {'unique_together': "(('period', 'entity', 'type'),)", 'object_name': 'ProvidedServicesReport'},
            '_status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'client_hiv_counselling': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'client_hiv_positive': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'client_hiv_tested': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'unfpa_core_providedservicesreport_reports'", 'to': "orm['bolibana.Provider']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'emergency_contraception': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'unfpa_core_providedservicesreport_reports'", 'to': "orm['bolibana.Entity']"}),
            'female_condom': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'implant': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'implant_removal': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'injectable': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'iud': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'iud_removal': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'male_condom': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolibana.Provider']", 'null': 'True', 'blank': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'new_client': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'oral_pills': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'unfpa_core_providedservicesreport_reports'", 'to': "orm['bolibana.Period']"}),
            'pf_first_time': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pf_visit_ams_ticket': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pf_visit_long_term': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pf_visit_o25': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pf_visit_provider_ticket': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pf_visit_short_term': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pf_visit_u25': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'receipt': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'blank': 'True'}),
            'returning_client': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'sources': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['unfpa_core.ProvidedServicesReport']", 'null': 'True', 'blank': 'True'}),
            'total_hiv_test': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'unfpa_core.rhcommoditiesreport': {
            'Meta': {'unique_together': "(('period', 'entity', 'type'),)", 'object_name': 'RHCommoditiesReport'},
            '_status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'amoxicillin_cap_gel': ('django.db.models.fields.IntegerField', [], {}),
            'amoxicillin_ij': ('django.db.models.fields.IntegerField', [], {}),
            'amoxicillin_suspension': ('django.db.models.fields.IntegerField', [], {}),
            'azithromycine_suspension': ('django.db.models.fields.IntegerField', [], {}),
            'azithromycine_tab': ('django.db.models.fields.IntegerField', [], {}),
            'benzathine_penicillin': ('django.db.models.fields.IntegerField', [], {}),
            'cefexime': ('django.db.models.fields.IntegerField', [], {}),
            'clotrimazole': ('django.db.models.fields.IntegerField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'unfpa_core_rhcommoditiesreport_reports'", 'to': "orm['bolibana.Provider']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'delivery_services': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'unfpa_core_rhcommoditiesreport_reports'", 'to': "orm['bolibana.Entity']"}),
            'ergometrine_tab': ('django.db.models.fields.IntegerField', [], {}),
            'ergometrine_vials': ('django.db.models.fields.IntegerField', [], {}),
            'family_planning': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'female_condom': ('django.db.models.fields.IntegerField', [], {}),
            'female_sterilization': ('django.db.models.fields.IntegerField', [], {}),
            'folate': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'implants': ('django.db.models.fields.IntegerField', [], {}),
            'injectable': ('django.db.models.fields.IntegerField', [], {}),
            'iron': ('django.db.models.fields.IntegerField', [], {}),
            'iron_folate': ('django.db.models.fields.IntegerField', [], {}),
            'iud': ('django.db.models.fields.IntegerField', [], {}),
            'magnesium_sulfate': ('django.db.models.fields.IntegerField', [], {}),
            'male_condom': ('django.db.models.fields.IntegerField', [], {}),
            'male_sterilization': ('django.db.models.fields.IntegerField', [], {}),
            'metronidazole': ('django.db.models.fields.IntegerField', [], {}),
            'modified_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bolibana.Provider']", 'null': 'True', 'blank': 'True'}),
            'modified_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'oral_pills': ('django.db.models.fields.IntegerField', [], {}),
            'oxytocine': ('django.db.models.fields.IntegerField', [], {}),
            'period': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'unfpa_core_rhcommoditiesreport_reports'", 'to': "orm['bolibana.Period']"}),
            'receipt': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'blank': 'True'}),
            'sources': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['unfpa_core.RHCommoditiesReport']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'unfpa_core.uentity': {
            'Meta': {'object_name': 'UEntity', '_ormbases': ['bolibana.Entity']},
            'entity_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['bolibana.Entity']", 'unique': 'True', 'primary_key': 'True'}),
            'is_credos': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_unfpa': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['unfpa_core']
