class Vendor:
    def __init__(self, id, name, labor_types, cost, products, itq_d90, active_d90, operating_systems, remote_only,
                 target_customer_sizes, required_products=[], no_small_jobs=False, service_minimum_minutes=0):
        self.id = id
        self.name = name
        self.labor_types = labor_types
        self.cost = cost
        self.service_minimum_minutes = service_minimum_minutes
        self.target_customer_sizes = target_customer_sizes
        self.products = products
        self.required_products = required_products
        self.itq_d90 = itq_d90
        self.active_d90 = active_d90
        self.no_small_jobs = no_small_jobs
        self.operating_systems = operating_systems
        self.remote_only = remote_only

    def __str__(self):
        return "id: {}, name: {}, labor_types: {}, cost: {}, service_minimum_minutes: {}, products: {}, " \
               "required_products: {}, itq_d90: {}, active_d90: {}, no_small_jobs: {}, operating_systems: {}, " \
               "remote_only: {}, target_customer_sizes: {}"\
            .format(self.id, self.name, self.labor_types, self.cost, self.service_minimum_minutes, self.products,
                    self.required_products, self.itq_d90, self.active_d90, self.no_small_jobs, self.operating_systems,
                    self.remote_only, self.target_customer_sizes)


class Company:
    def __init__(self, id, size, max_cost, labor_type):
        self.id = id
        self.size = size
        self.max_cost = max_cost
        self.labor_type = labor_type

    def __str__(self):
        return "id: {}, size: {}, max_cost: {}, labor_type: {}"\
            .format(self.id, self.size, self.max_cost, self.labor_type)


class Order:
    matched_vendor_ids = []

    def __init__(self, id, company_id, product, operating_system, minimum_time_required, on_site):
        self.id = id
        self.company_id = company_id
        self.product = product
        self.operating_system = operating_system
        self.minimum_time_required = minimum_time_required
        self.on_site = on_site

    def __str__(self):
        return "id: {}, company_id: {}, product: {}, operating_system: {}, minimum_time_required: {}, on_site: {}"\
            .format(self.id, self.company_id, self.product, self.operating_system, self.minimum_time_required, self.on_site)
