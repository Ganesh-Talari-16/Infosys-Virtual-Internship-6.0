# quizzes/management/commands/seed_categories.py
"""
Django management command to seed categories and subcategories.
"""
from django.core.management.base import BaseCommand
from quizzes.models import Category, SubCategory


class Command(BaseCommand):
    help = 'Seed the database with sample categories and subcategories'

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing categories...')
        Category.objects.all().delete()
        
        self.stdout.write('Seeding categories...')
        
        # ======================
        # ACADEMICS
        # ======================
        academics = Category.objects.create(
            name='Academics',
            description='Academic subjects and educational topics'
        )
        
        # Engineering (Level 1)
        engineering = SubCategory.objects.create(
            category=academics,
            name='Engineering',
            level=1,
            is_leaf=False,
            description='Engineering streams and subjects'
        )
        
        # CSE (Level 2)
        cse = SubCategory.objects.create(
            category=academics,
            name='CSE',
            level=2,
            parent_subcat=engineering,
            is_leaf=False,
            description='Computer Science & Engineering'
        )
        
        # CSE Subjects (Level 3 - Leaf nodes)
        for subj in ['Java', 'Python', 'Operating Systems', 'Data Structures', 'DBMS']:
            SubCategory.objects.create(
                category=academics,
                name=subj,
                level=3,
                parent_subcat=cse,
                is_leaf=True,
                description=f'{subj} programming and concepts'
            )
        
        # AIML (Level 2)
        aiml = SubCategory.objects.create(
            category=academics,
            name='AIML',
            level=2,
            parent_subcat=engineering,
            is_leaf=False,
            description='Artificial Intelligence & Machine Learning'
        )
        
        # AIML Subjects (Level 3 - Leaf nodes)
        for subj in ['Machine Learning', 'Deep Learning', 'Neural Networks', 'NLP']:
            SubCategory.objects.create(
                category=academics,
                name=subj,
                level=3,
                parent_subcat=aiml,
                is_leaf=True,
                description=f'{subj} concepts and applications'
            )
        
        # Medical (Level 1)
        medical = SubCategory.objects.create(
            category=academics,
            name='Medical',
            level=1,
            is_leaf=False,
            description='Medical science subjects'
        )
        
        # Medical Subjects (Level 2 - Leaf nodes)
        for subj in ['Anatomy', 'Physiology', 'Biochemistry', 'Pharmacology']:
            SubCategory.objects.create(
                category=academics,
                name=subj,
                level=2,
                parent_subcat=medical,
                is_leaf=True,
                description=f'{subj} studies'
            )
        
        # ======================
        # ENTERTAINMENT
        # ======================
        entertainment = Category.objects.create(
            name='Entertainment',
            description='Movies, music, and pop culture'
        )
        
        # Entertainment subcategories (Leaf nodes directly)
        for subj, desc in [
            ('Movies', 'Film trivia and cinema'),
            ('Music', 'Songs, artists, and genres'),
            ('TV Shows', 'Television series and shows'),
            ('Gaming', 'Video games and esports')
        ]:
            SubCategory.objects.create(
                category=entertainment,
                name=subj,
                level=1,
                is_leaf=True,
                description=desc
            )
        
        # ======================
        # GENERAL KNOWLEDGE
        # ======================
        gk = Category.objects.create(
            name='General Knowledge',
            description='World facts, history, and current affairs'
        )
        
        # GK subcategories (Leaf nodes directly)
        for subj, desc in [
            ('History', 'World and regional history'),
            ('Geography', 'Countries, capitals, and landmarks'),
            ('Science', 'Scientific discoveries and facts'),
            ('Current Affairs', 'Recent news and events'),
            ('Sports', 'Sports events and athletes')
        ]:
            SubCategory.objects.create(
                category=gk,
                name=subj,
                level=1,
                is_leaf=True,
                description=desc
            )
        
        # Summary
        cat_count = Category.objects.count()
        sub_count = SubCategory.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully seeded {cat_count} categories and {sub_count} subcategories!'
            )
        )
