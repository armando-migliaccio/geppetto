# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        config_cls = orm.ConfigClass.objects.create(name='geppetto-backend-config',
                                                    description='Configuration of the Geppetto backend. Internal use only.')
        init_cls = orm.ConfigClass.objects.create(name='ensure-geppetto-init-run',
                                                    description='To setup the Geppetto backend. Internal use only.')
        backend_type = orm.ConfigClassParameterType.objects.create(name='geppettodb_backend',
                                                                  validator_function='enum_validator',
                                                                  validator_kwargs='sqlite3=0,mysql=1')

        string_type = orm.ConfigClassParameterType.objects.get(id=13)
        fqdn_type = orm.ConfigClassParameterType.objects.get(id=2)
        configs = {'VPX_MASTER_DB_BACKEND': {'default_value': 'sqlite3',
                                             'config_type': backend_type,
                                             'description': 'The DB driver. Internal use only.',
                                             },
                   'VPX_MASTER_DB_NAME': {'default_value': '/var/lib/geppetto/sqlite3.db~',
                                             'config_type': string_type,
                                             'description': 'The DB name. Valid only if DB_BACKEND != sqlite3. Internal use only.', },
                   'VPX_MASTER_DB_HOST': {'default_value': '',
                                             'config_type': fqdn_type,
                                             'description': 'The DB host fqdn. Valid only if DB_BACKEND != sqlite3. Internal use only.', },
                   'VPX_MASTER_DB_USER': {'default_value': '',
                                             'config_type': string_type,
                                             'description': 'The DB user. Valid only if DB_BACKEND != sqlite3. Internal use only.', },
                   'VPX_MASTER_DB_PASS': {'default_value': '',
                                             'config_type': string_type,
                                             'description': 'The user password. Valid only if DB_BACKEND != sqlite3. Internal use only.', },
                   'VPX_MASTER_QUEUE_HOST': {'default_value': 'localhost',
                                             'config_type': fqdn_type,
                                             'description': 'The Message Queue fqdn. Internal use only.', },
                   'VPX_MASTER_QUEUE_USER': {'default_value': 'guest',
                                             'config_type': string_type,
                                             'description': 'The Queue user. Internal use only.', },
                   'VPX_MASTER_QUEUE_PASS': {'default_value': 'guest',
                                             'config_type': string_type,
                                             'description': 'The user password. Internal use only.', }, }
        for k, d in configs.iteritems():
            orm.ConfigClassParameter.\
                objects.create(name=k,
                               default_value=d['default_value'],
                               config_type=d['config_type'],
                               description=d['description'],
                               config_class=config_cls)

        celery_role = orm.Role.objects.get(id='29')
        orm.RoleConfigClassAssignment.objects.create(role=celery_role,
                                                     config_class=config_cls)
        orm.RoleConfigClassAssignment.objects.create(role=celery_role,
                                                     config_class=init_cls)

    def backwards(self, orm):
        raise NotImplementedError()


    models = {
        'core.configclass': {
            'Meta': {'ordering': "['name']", 'object_name': 'ConfigClass'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'core.configclassparameter': {
            'Meta': {'ordering': "['name']", 'object_name': 'ConfigClassParameter'},
            'config_class': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ConfigClass']"}),
            'config_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ConfigClassParameterType']", 'null': 'True', 'blank': 'True'}),
            'default_value': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'core.configclassparametertype': {
            'Meta': {'ordering': "['name']", 'object_name': 'ConfigClassParameterType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'validator_function': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'validator_kwargs': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'core.group': {
            'Meta': {'ordering': "['name']", 'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'})
        },
        'core.groupoverride': {
            'Meta': {'ordering': "['group']", 'unique_together': "(('group', 'config_class_parameter'),)", 'object_name': 'GroupOverride'},
            'config_class_parameter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ConfigClassParameter']"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'core.host': {
            'Meta': {'ordering': "['fqdn']", 'object_name': 'Host'},
            'address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'blank': 'True'}),
            'fqdn': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '12', 'blank': 'True'})
        },
        'core.master': {
            'Meta': {'ordering': "['fqdn']", 'object_name': 'Master'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fqdn': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'promoted_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'core.node': {
            'Meta': {'ordering': "['fqdn']", 'object_name': 'Node'},
            'facts': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'facts_list': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fqdn': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Group']", 'null': 'True', 'blank': 'True'}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Host']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joined_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Master']"}),
            'report': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'report_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'report_last_changed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'report_log': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'report_status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'roles': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Role']", 'through': "orm['core.NodeRoleAssignment']", 'symmetrical': 'False'})
        },
        'core.noderoleassignment': {
            'Meta': {'ordering': "['node']", 'unique_together': "(('role', 'node'),)", 'object_name': 'NodeRoleAssignment'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Node']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Role']"})
        },
        'core.override': {
            'Meta': {'ordering': "['node']", 'unique_together': "(('node', 'config_class_parameter'),)", 'object_name': 'Override'},
            'config_class_parameter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ConfigClassParameter']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Node']"}),
            'one_time_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'core.role': {
            'Meta': {'ordering': "['name']", 'object_name': 'Role'},
            'config_classes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.ConfigClass']", 'through': "orm['core.RoleConfigClassAssignment']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.RoleDescription']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'}),
            'service': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'core.roleconfigclassassignment': {
            'Meta': {'ordering': "['role']", 'unique_together': "(('role', 'config_class'),)", 'object_name': 'RoleConfigClassAssignment', 'db_table': "'core_roleconfigclassassignement'"},
            'config_class': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ConfigClass']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Role']"})
        },
        'core.roledesconfigparamassignment': {
            'Meta': {'ordering': "['role_description']", 'unique_together': "(('config_parameter', 'role_description'),)", 'object_name': 'RoleDesConfigParamAssignment'},
            'config_parameter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.ConfigClassParameter']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role_description': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.RoleDescription']"})
        },
        'core.roledescription': {
            'Meta': {'ordering': "['name']", 'object_name': 'RoleDescription'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'})
        }
    }

    complete_apps = ['core']