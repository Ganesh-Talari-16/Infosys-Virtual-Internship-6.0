# quizzes/views_spa.py
"""
SPA views for dynamic quiz category selection.
"""
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Category, SubCategory


@login_required
def quiz_selector_view(request):
    """
    Render the SPA template with initial categories.
    """
    categories = Category.objects.all().order_by('name')
    return render(request, 'quizzes/quiz_selector.html', {
        'categories': categories
    })


@login_required
def get_children_ajax(request):
    """
    AJAX endpoint to get children for a given node.
    
    Query params:
        - node_type: 'category' or 'subcategory'
        - node_id: ID of the parent node
    
    Returns JSON:
        {
            "children": [{"id": 1, "name": "...", "is_leaf": false}, ...],
            "parent_name": "Category Name"
        }
    """
    node_type = request.GET.get('node_type')
    node_id = request.GET.get('node_id')
    
    if not node_type or not node_id:
        return JsonResponse({'error': 'Missing parameters'}, status=400)
    
    children = []
    parent_name = ""
    
    if node_type == 'category':
        # Get level-1 subcategories for this category
        category = get_object_or_404(Category, id=node_id)
        parent_name = category.name
        subcats = SubCategory.objects.filter(
            category=category,
            parent_subcat__isnull=True
        ).order_by('name')
        
        for sub in subcats:
            children.append({
                'id': sub.id,
                'name': sub.name,
                'is_leaf': sub.is_leaf,
                'description': sub.description or ''
            })
    
    elif node_type == 'subcategory':
        # Get child subcategories for this subcategory
        parent_sub = get_object_or_404(SubCategory, id=node_id)
        parent_name = parent_sub.name
        child_subs = SubCategory.objects.filter(
            parent_subcat=parent_sub
        ).order_by('name')
        
        for sub in child_subs:
            children.append({
                'id': sub.id,
                'name': sub.name,
                'is_leaf': sub.is_leaf,
                'description': sub.description or ''
            })
    
    return JsonResponse({
        'children': children,
        'parent_name': parent_name
    })
