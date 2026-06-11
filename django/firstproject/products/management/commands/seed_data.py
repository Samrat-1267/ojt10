from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from products.models import Category, Product, Review
from accounts.models import UserProfile


class Command(BaseCommand):
    help = 'Seeds the database with sample products, categories, and demo data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@techforge.com', 'admin123')
            self.stdout.write(f'  Created admin user: admin / admin123')

        if not User.objects.filter(username='demo').exists():
            demo = User.objects.create_user('demo', 'demo@techforge.com', 'demo123')
            UserProfile.objects.get_or_create(user=demo)
            self.stdout.write(f'  Created demo user: demo / demo123')

        categories_data = [
            {'name': 'PC Components', 'slug': 'components', 'is_component_category': True, 'order': 1, 'children': [
                {'name': 'CPUs', 'slug': 'cpus', 'is_component_category': True, 'order': 1},
                {'name': 'GPUs', 'slug': 'gpus', 'is_component_category': True, 'order': 2},
                {'name': 'Motherboards', 'slug': 'motherboards', 'is_component_category': True, 'order': 3},
                {'name': 'RAM', 'slug': 'ram', 'is_component_category': True, 'order': 4},
                {'name': 'Storage', 'slug': 'storage', 'is_component_category': True, 'order': 5},
                {'name': 'Power Supplies', 'slug': 'power-supplies', 'is_component_category': True, 'order': 6},
                {'name': 'Cooling', 'slug': 'cooling', 'is_component_category': True, 'order': 7},
                {'name': 'Cases', 'slug': 'cases', 'is_component_category': True, 'order': 8},
            ]},
            {'name': 'Gaming Accessories', 'slug': 'accessories', 'is_component_category': False, 'order': 2, 'children': [
                {'name': 'Keyboards', 'slug': 'keyboards', 'is_component_category': False, 'order': 1},
                {'name': 'Mice', 'slug': 'mice', 'is_component_category': False, 'order': 2},
                {'name': 'Headsets', 'slug': 'headsets', 'is_component_category': False, 'order': 3},
                {'name': 'Monitors', 'slug': 'monitors', 'is_component_category': False, 'order': 4},
                {'name': 'Mousepads', 'slug': 'mousepads', 'is_component_category': False, 'order': 5},
            ]},
            {'name': 'Custom PC Builds', 'slug': 'custom-builds', 'is_component_category': False, 'order': 3},
        ]

        for cat_data in categories_data:
            parent, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'is_component_category': cat_data['is_component_category'],
                    'order': cat_data['order'],
                }
            )
            if created:
                self.stdout.write(f'  Created category: {parent.name}')

            for child_data in cat_data.get('children', []):
                child, created = Category.objects.get_or_create(
                    slug=child_data['slug'],
                    defaults={
                        'name': child_data['name'],
                        'parent': parent,
                        'is_component_category': child_data['is_component_category'],
                        'order': child_data['order'],
                    }
                )
                if created:
                    self.stdout.write(f'  Created subcategory: {child.name}')

        cpu_cat = Category.objects.get(slug='cpus')
        gpu_cat = Category.objects.get(slug='gpus')
        mb_cat = Category.objects.get(slug='motherboards')
        ram_cat = Category.objects.get(slug='ram')
        storage_cat = Category.objects.get(slug='storage')
        psu_cat = Category.objects.get(slug='power-supplies')
        cooling_cat = Category.objects.get(slug='cooling')
        case_cat = Category.objects.get(slug='cases')
        kb_cat = Category.objects.get(slug='keyboards')
        mice_cat = Category.objects.get(slug='mice')
        headset_cat = Category.objects.get(slug='headsets')
        monitor_cat = Category.objects.get(slug='monitors')
        pad_cat = Category.objects.get(slug='mousepads')
        builds_cat = Category.objects.get(slug='custom-builds')

        products_data = [
            {'cat': cpu_cat, 'name': 'AMD Ryzen 9 7950X', 'slug': 'amd-ryzen-9-7950x', 'price': 699.99, 'stock': 25, 'featured': True, 'bestseller': True, 'ctype': 'cpu', 'specs': {'Cores': '16', 'Threads': '32', 'Base Clock': '4.5 GHz', 'Boost Clock': '5.7 GHz', 'TDP': '170W', 'Socket': 'AM5'}},
            {'cat': cpu_cat, 'name': 'Intel Core i9-14900K', 'slug': 'intel-core-i9-14900k', 'price': 589.99, 'stock': 18, 'featured': True, 'ctype': 'cpu', 'specs': {'Cores': '24 (8P + 16E)', 'Threads': '32', 'Max Turbo': '6.0 GHz', 'TDP': '253W', 'Socket': 'LGA 1700'}},
            {'cat': cpu_cat, 'name': 'AMD Ryzen 7 7800X3D', 'slug': 'amd-ryzen-7-7800x3d', 'price': 449.99, 'stock': 30, 'bestseller': True, 'ctype': 'cpu', 'specs': {'Cores': '8', 'Threads': '16', 'Base Clock': '4.2 GHz', 'Boost Clock': '5.0 GHz', 'Cache': '96MB 3D V-Cache', 'Socket': 'AM5'}},
            {'cat': cpu_cat, 'name': 'Intel Core i5-14600K', 'slug': 'intel-core-i5-14600k', 'price': 319.99, 'stock': 22, 'ctype': 'cpu', 'specs': {'Cores': '14 (6P + 8E)', 'Threads': '20', 'Max Turbo': '5.3 GHz', 'TDP': '181W', 'Socket': 'LGA 1700'}},
            {'cat': gpu_cat, 'name': 'NVIDIA GeForce RTX 4090', 'slug': 'nvidia-rtx-4090', 'price': 1799.99, 'stock': 5, 'featured': True, 'bestseller': True, 'ctype': 'gpu', 'specs': {'CUDA Cores': '16384', 'VRAM': '24GB GDDR6X', 'Boost Clock': '2.52 GHz', 'TDP': '450W', 'Interface': 'PCIe 4.0 x16'}},
            {'cat': gpu_cat, 'name': 'AMD Radeon RX 7900 XTX', 'slug': 'amd-rx-7900-xtx', 'price': 999.99, 'stock': 12, 'featured': True, 'ctype': 'gpu', 'specs': {'Compute Units': '96', 'VRAM': '24GB GDDR6', 'Game Clock': '2.3 GHz', 'TDP': '355W', 'Interface': 'PCIe 4.0 x16'}},
            {'cat': gpu_cat, 'name': 'NVIDIA GeForce RTX 4070 Ti', 'slug': 'nvidia-rtx-4070-ti', 'price': 799.99, 'stock': 15, 'bestseller': True, 'ctype': 'gpu', 'specs': {'CUDA Cores': '7680', 'VRAM': '12GB GDDR6X', 'Boost Clock': '2.61 GHz', 'TDP': '285W'}},
            {'cat': gpu_cat, 'name': 'NVIDIA GeForce RTX 4060', 'slug': 'nvidia-rtx-4060', 'price': 299.99, 'stock': 20, 'ctype': 'gpu', 'specs': {'CUDA Cores': '3072', 'VRAM': '8GB GDDR6', 'Boost Clock': '2.46 GHz', 'TDP': '115W'}},
            {'cat': mb_cat, 'name': 'ASUS ROG Crosshair X670E Hero', 'slug': 'asus-rog-crosshair-x670e', 'price': 499.99, 'stock': 8, 'featured': True, 'ctype': 'motherboard', 'specs': {'Socket': 'AM5', 'Chipset': 'X670E', 'Form Factor': 'ATX', 'RAM Slots': '4x DDR5', 'PCIe Slots': '2x PCIe 5.0 x16'}},
            {'cat': mb_cat, 'name': 'MSI MAG Z790 Tomahawk', 'slug': 'msi-mag-z790-tomahawk', 'price': 259.99, 'stock': 14, 'bestseller': True, 'ctype': 'motherboard', 'specs': {'Socket': 'LGA 1700', 'Chipset': 'Z790', 'Form Factor': 'ATX', 'RAM Slots': '4x DDR5', 'PCIe Slots': '1x PCIe 5.0 x16'}},
            {'cat': ram_cat, 'name': 'G.Skill Trident Z5 RGB 32GB DDR5-6000', 'slug': 'gskill-trident-z5-32gb-ddr5', 'price': 119.99, 'stock': 35, 'bestseller': True, 'ctype': 'ram', 'specs': {'Capacity': '32GB (2x16GB)', 'Type': 'DDR5-6000', 'Timings': 'CL30-38-38-96', 'Voltage': '1.35V', 'RGB': 'Yes'}},
            {'cat': ram_cat, 'name': 'Corsair Vengeance 64GB DDR5-5600', 'slug': 'corsair-vengeance-64gb-ddr5', 'price': 199.99, 'stock': 20, 'ctype': 'ram', 'specs': {'Capacity': '64GB (2x32GB)', 'Type': 'DDR5-5600', 'Timings': 'CL40', 'RGB': 'No'}},
            {'cat': storage_cat, 'name': 'Samsung 990 Pro 2TB NVMe SSD', 'slug': 'samsung-990-pro-2tb', 'price': 249.99, 'stock': 28, 'featured': True, 'bestseller': True, 'ctype': 'storage', 'specs': {'Capacity': '2TB', 'Interface': 'PCIe 4.0 NVMe M.2', 'Seq Read': '7,450 MB/s', 'Seq Write': '6,900 MB/s'}},
            {'cat': storage_cat, 'name': 'WD Black SN850X 1TB', 'slug': 'wd-black-sn850x-1tb', 'price': 139.99, 'stock': 30, 'ctype': 'storage', 'specs': {'Capacity': '1TB', 'Interface': 'PCIe 4.0 NVMe M.2', 'Seq Read': '7,300 MB/s', 'Seq Write': '6,300 MB/s'}},
            {'cat': storage_cat, 'name': 'Seagate Barracuda 2TB HDD', 'slug': 'seagate-barracuda-2tb', 'price': 64.99, 'stock': 50, 'ctype': 'storage', 'specs': {'Capacity': '2TB', 'Interface': 'SATA III', 'RPM': '7200', 'Cache': '256MB'}},
            {'cat': psu_cat, 'name': 'Corsair RM1000x Shift 1000W', 'slug': 'corsair-rm1000x-shift', 'price': 189.99, 'stock': 12, 'featured': True, 'ctype': 'psu', 'specs': {'Wattage': '1000W', 'Rating': '80+ Gold', 'Modular': 'Fully Modular', 'Form Factor': 'ATX'}},
            {'cat': psu_cat, 'name': 'EVGA SuperNOVA 850 G7', 'slug': 'evga-supernova-850-g7', 'price': 149.99, 'stock': 18, 'ctype': 'psu', 'specs': {'Wattage': '850W', 'Rating': '80+ Gold', 'Modular': 'Fully Modular', 'Form Factor': 'ATX'}},
            {'cat': cooling_cat, 'name': 'Corsair iCUE H150i Elite LCD XT', 'slug': 'corsair-h150i-elite-lcd', 'price': 259.99, 'stock': 10, 'featured': True, 'ctype': 'cooling', 'specs': {'Type': '360mm AIO Liquid Cooler', 'Fan Size': '3x 120mm', 'RGB': 'Yes', 'LCD Display': 'Yes'}},
            {'cat': cooling_cat, 'name': 'Noctua NH-D15 Chromax Black', 'slug': 'noctua-nh-d15-chromax', 'price': 119.99, 'stock': 15, 'bestseller': True, 'ctype': 'cooling', 'specs': {'Type': 'Dual Tower Air Cooler', 'Fan Size': '2x 140mm', 'TDP': '250W+', 'Noise': '24.6 dBA'}},
            {'cat': case_cat, 'name': 'Lian Li O11 Dynamic EVO', 'slug': 'lian-li-o11-dynamic-evo', 'price': 179.99, 'stock': 8, 'featured': True, 'ctype': 'case', 'specs': {'Form Factor': 'Mid Tower', 'Motherboard Support': 'E-ATX, ATX, mATX', 'GPU Clearance': '420mm', 'Cooler Clearance': '167mm'}},
            {'cat': case_cat, 'name': 'Corsair 5000D Airflow', 'slug': 'corsair-5000d-airflow', 'price': 149.99, 'stock': 14, 'ctype': 'case', 'specs': {'Form Factor': 'Mid Tower', 'Motherboard Support': 'ATX, mATX, Mini-ITX', 'GPU Clearance': '420mm', 'Cooler Clearance': '170mm'}},
            {'cat': kb_cat, 'name': 'Wooting 60HE+', 'slug': 'wooting-60he-plus', 'price': 199.99, 'stock': 20, 'featured': True, 'bestseller': True, 'specs': {'Switch Type': 'Lekker V2 Magnetic', 'Form Factor': '60%', 'RGB': 'Per-Key', 'Hot-Swappable': 'Yes', 'Polling Rate': '8000Hz'}},
            {'cat': kb_cat, 'name': 'Keychron Q1 Pro', 'slug': 'keychron-q1-pro', 'price': 219.99, 'stock': 15, 'specs': {'Switch Type': 'Gateron Jupiter', 'Form Factor': '75%', 'RGB': 'South-Facing', 'Connectivity': 'Wireless/Wired', 'Material': 'Aluminum'}},
            {'cat': kb_cat, 'name': 'Logitech G Pro X TKL', 'slug': 'logitech-g-pro-x-tkl', 'price': 179.99, 'stock': 22, 'bestseller': True, 'specs': {'Switch Type': 'GX Blue/Brown/Red', 'Form Factor': 'TKL', 'RGB': 'LIGHTSYNC', 'Lightspeed Wireless': 'Yes'}},
            {'cat': mice_cat, 'name': 'Razer DeathAdder V3 Pro', 'slug': 'razer-deathadder-v3-pro', 'price': 149.99, 'stock': 25, 'bestseller': True, 'specs': {'Sensor': 'Focus Pro 30K', 'DPI': '30,000', 'Weight': '63g', 'Battery': '90 Hours', 'Connectivity': 'Wireless'}},
            {'cat': mice_cat, 'name': 'Logitech G Pro X Superlight 2', 'slug': 'logitech-g-pro-x-superlight-2', 'price': 159.99, 'stock': 18, 'featured': True, 'specs': {'Sensor': 'HERO 2', 'DPI': '32,000', 'Weight': '60g', 'Battery': '95 Hours', 'Connectivity': 'LIGHTSPEED Wireless'}},
            {'cat': mice_cat, 'name': 'Pulsar X2H Mini', 'slug': 'pulsar-x2h-mini', 'price': 89.99, 'stock': 30, 'specs': {'Sensor': 'PAW3395', 'DPI': '26,000', 'Weight': '52g', 'Connectivity': 'Wireless'}},
            {'cat': headset_cat, 'name': 'SteelSeries Arctis Nova Pro', 'slug': 'steelseries-arctis-nova-pro', 'price': 349.99, 'stock': 10, 'featured': True, 'specs': {'Driver': '40mm Neodymium', 'Frequency Response': '20-22,000 Hz', 'Microphone': 'AI-Powered Noise Cancellation', 'Connectivity': 'USB/3.5mm/Bluetooth'}},
            {'cat': headset_cat, 'name': 'Logitech G Pro X Wireless', 'slug': 'logitech-g-pro-x-wireless', 'price': 229.99, 'stock': 14, 'specs': {'Driver': '50mm PRO-G', 'Surround Sound': 'DTS 7.1', 'Microphone': 'Blue VO!CE', 'Battery': '20+ Hours'}},
            {'cat': monitor_cat, 'name': 'Alienware AW3423DWF QD-OLED', 'slug': 'alienware-aw3423dwf', 'price': 1099.99, 'stock': 5, 'featured': True, 'bestseller': True, 'specs': {'Size': '34"', 'Resolution': '3440x1440 UWQHD', 'Panel': 'QD-OLED', 'Refresh Rate': '165Hz', 'Response Time': '0.1ms GtG'}},
            {'cat': monitor_cat, 'name': 'LG 27GP950-B UltraGear', 'slug': 'lg-27gp950-b', 'price': 799.99, 'stock': 8, 'specs': {'Size': '27"', 'Resolution': '3840x2160 4K', 'Panel': 'Nano IPS', 'Refresh Rate': '160Hz', 'Response Time': '1ms GtG'}},
            {'cat': pad_cat, 'name': 'Artisan Hien XL', 'slug': 'artisan-hien-xl', 'price': 64.99, 'stock': 40, 'bestseller': True, 'specs': {'Size': 'XL (490x420mm)', 'Surface': 'Hybrid Cloth', 'Thickness': '4mm', 'Base': 'Natural Rubber'}},
            {'cat': pad_cat, 'name': 'Lethal Gaming Gear Saturn Pro', 'slug': 'lgg-saturn-pro', 'price': 39.99, 'stock': 50, 'specs': {'Size': 'XL (500x500mm)', 'Surface': 'Cloth', 'Thickness': '4mm', 'Stitched Edges': 'Yes'}},
        ]

        for pd in products_data:
            product, created = Product.objects.get_or_create(
                slug=pd['slug'],
                defaults={
                    'category': pd['cat'],
                    'name': pd['name'],
                    'description': f'The {pd["name"]} delivers exceptional performance for gaming and professional workloads.',
                    'price': pd['price'],
                    'stock': pd['stock'],
                    'is_featured': pd.get('featured', False),
                    'is_best_seller': pd.get('bestseller', False),
                    'component_type': pd.get('ctype'),
                    'specifications': pd.get('specs', {}),
                }
            )
            if created:
                self.stdout.write(f'  Created product: {product.name} (${product.price})')

        custom_builds = [
            {'cat': builds_cat, 'name': 'The Ultimate Gaming Rig', 'slug': 'ultimate-gaming-rig', 'price': 4999.99, 'stock': 3, 'featured': True, 'specs': {'CPU': 'AMD Ryzen 9 7950X', 'GPU': 'RTX 4090', 'RAM': '64GB DDR5', 'Storage': '2TB NVMe + 4TB HDD', 'Cooling': 'Custom Loop'}},
            {'cat': builds_cat, 'name': 'Streamer Pro Build', 'slug': 'streamer-pro-build', 'price': 3499.99, 'stock': 5, 'featured': True, 'specs': {'CPU': 'Intel Core i9-14900K', 'GPU': 'RTX 4080', 'RAM': '64GB DDR5', 'Storage': '2TB NVMe', 'Cooling': '360mm AIO'}},
            {'cat': builds_cat, 'name': 'Value Gaming Build', 'slug': 'value-gaming-build', 'price': 1499.99, 'stock': 8, 'specs': {'CPU': 'AMD Ryzen 5 7600', 'GPU': 'RTX 4060', 'RAM': '32GB DDR5', 'Storage': '1TB NVMe', 'Cooling': 'Air Cooler'}},
        ]

        for build in custom_builds:
            product, created = Product.objects.get_or_create(
                slug=build['slug'],
                defaults={
                    'category': build['cat'],
                    'name': build['name'],
                    'description': f'Pre-built {build["name"]} - professionally assembled and tested.',
                    'price': build['price'],
                    'stock': build['stock'],
                    'is_featured': build.get('featured', False),
                    'is_custom_build': True,
                    'specifications': build.get('specs', {}),
                }
            )
            if created:
                self.stdout.write(f'  Created custom build: {product.name}')

        if User.objects.filter(username='demo').exists():
            demo = User.objects.get(username='demo')
            products = Product.objects.all()[:10]
            for product in products:
                Review.objects.get_or_create(
                    product=product,
                    user=demo,
                    defaults={
                        'rating': 5 if product.is_featured else 4,
                        'comment': f'Great {product.name}! Performance is amazing, highly recommended for anyone building a new PC.',
                    }
                )
            for product in Product.objects.all()[10:20]:
                Review.objects.get_or_create(
                    product=product,
                    user=demo,
                    defaults={
                        'rating': 4,
                        'comment': 'Solid product, works as expected. Fast shipping and great packaging.',
                    }
                )
            self.stdout.write('  Created sample reviews')

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
        self.stdout.write('')
        self.stdout.write('Admin login:   admin / admin123')
        self.stdout.write('Demo login:    demo / demo123')
