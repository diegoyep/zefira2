import datetime

benefit = dict(
            'title': '',
            'description': '',
            'date_published' : '',
            'active': '',
            'company_name': '',
            'dates_reserved': [],
            'dates_validated': [],
            'times_reserved': 0,
            'times_validated': 0 ,
            'picture_id': '',
            'type' :'',
            )
            
client = dict(
            '_id':'',
            'username': '',
            'password': '',
            'info': {
                        'name':'',
                        'email':'',                     
                    },
            'interests': [],
            'reserves' : [],
            'validated': [],       
            'companies_followd': 0,
            'benefits_reserved': 0,
            'benefits_validated': 0,
            'dates_reserves': [],
            'dates_validated': [],
            'dates_followd': [],
            'geolocation': '',
            'membership_type': '',
            'membership_join': '',
            'membership_end' : '',
            'friends': [],
            'groups': [
                        {
                            'ref':'',
                            'group_lead': '',
                        }
                      ],
            'profile_pic_id':''
            )
            
company = dict(

            '_id': '',
            'username': '',
            'info':
                {
                    'company_name':'',
                    'company_type': '',
                    'company_description': '',
                    'contact_info':
                                {
                                    'phone1': '',
                                    'phone2': '',
                                    'email' : ''
                                }
                    'picture_logo_id': ''
                },
             'benefits': [],
             'benefits_published': 0,
             'membership_type': '',
             'membership_join': '',
             'membership_end' : '',
             'levels':{
                        user_1 : {
                               'username': '',
                               'password': '',
                               'admin':'',
                               'privileges': []       
                                 },
                        user_2 : {}
                      },
             
              )
            
            
            
            
