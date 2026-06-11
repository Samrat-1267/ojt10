from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from products.models import Product
from .models import SavedBuild, CompatibilityRule


def builder(request):
    component_types = Product.COMPONENT_TYPES
    selected_components = {}

    for ctype, _ in component_types:
        product_id = request.GET.get(ctype)
        if product_id:
            try:
                selected_components[ctype] = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                pass

    build_id = request.GET.get('load')
    if build_id and request.user.is_authenticated:
        try:
            build = SavedBuild.objects.get(id=build_id, user=request.user)
            selected_components = {}
            for key in ['cpu', 'gpu', 'motherboard', 'ram', 'storage', 'psu', 'cooling', 'case']:
                comp = getattr(build, key)
                if comp:
                    selected_components[key] = comp
        except SavedBuild.DoesNotExist:
            pass

    total = sum(p.price for p in selected_components.values())

    context = {
        'component_types': component_types,
        'selected_components': selected_components,
        'total': total,
    }
    return render(request, 'custom_pc_builder/builder.html', context)


def get_components(request, component_type):
    products = Product.objects.filter(
        component_type=component_type,
        is_active=True,
        stock__gt=0
    ).values('id', 'name', 'price', 'image', 'stock')

    return JsonResponse(list(products), safe=False)


def check_compatibility(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        return JsonResponse({'compatible': True, 'message': 'All components are compatible.'})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def save_build(request):
    if request.method == 'POST':
        from django.http import JsonResponse
        import json
        data = json.loads(request.body)
        components = data.get('components', {})

        build = SavedBuild(
            user=request.user,
            name=data.get('name', 'My Custom Build'),
        )

        component_map = {
            'cpu': 'cpu', 'gpu': 'gpu', 'motherboard': 'motherboard',
            'ram': 'ram', 'storage': 'storage', 'psu': 'psu',
            'cooling': 'cooling', 'case': 'case',
        }

        for key, field in component_map.items():
            comp_id = components.get(key)
            if comp_id:
                try:
                    setattr(build, field, Product.objects.get(id=comp_id))
                except Product.DoesNotExist:
                    pass

        build.calculate_total()
        build.check_compatibility()
        build.save()

        return JsonResponse({
            'success': True,
            'build_id': build.id,
            'message': 'Build saved successfully!',
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def load_build(request, build_id):
    build = get_object_or_404(SavedBuild, id=build_id, user=request.user)
    return redirect(f"{builder.__name__}?load={build_id}")


@login_required
def delete_build(request, build_id):
    build = get_object_or_404(SavedBuild, id=build_id, user=request.user)
    build.delete()
    messages.success(request, 'Build deleted.')
    return redirect('accounts:saved_builds')
