import csv
import argparse
from heapq import heappush, heappop
import random

from models import Company, Order, Vendor
from constants import CompanySize, LaborType, OperatingSystem

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("vendor_csv")
    parser.add_argument("num_companies", type=int)
    parser.add_argument("num_orders", type=int)
    # parser.add_argument("epsilon")

    args = parser.parse_args()

    vendors, products, vendor_ids_to_itqd90 = load_vendors_from_csv(args.vendor_csv)

    print("------------INITIAL ITQ COUNTS------------")
    print(vendor_ids_to_itqd90)
    print()

    companies = generate_companies(args.num_companies)
    orders = generate_orders(args.num_orders, args.num_companies, products)
    initial_matches = simulate_matching(vendors, companies, orders)
    vendors_to_itq = get_vendors_to_itq(initial_matches, vendor_ids_to_itqd90)

    print("-------------ISSUED ITQS------------------")
    num_vendor_itqs = dict()
    for order_id, vendor_ids in vendors_to_itq.items():
        for vendor_id in vendor_ids:
            if vendor_id in num_vendor_itqs:
                num_vendor_itqs[vendor_id] = num_vendor_itqs[vendor_id] + 1
            else:
                num_vendor_itqs[vendor_id] = 0

        print("{Order:", orders[order_id], "}", vendor_ids)
    print()

    print("------------FINAL ITQ COUNTS--------------")
    print(vendor_ids_to_itqd90)
    print()

    print("-----------COUNT OF ISSUED ITQS-----------")
    for vendor_id, num_itqs in num_vendor_itqs.items():
        print(vendor_id, num_itqs)

def load_vendors_from_csv(vendor_csv_fpath):
    vendors = dict()
    all_products = set()
    vendor_ids_to_itqd90 = dict()

    with open(vendor_csv_fpath, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            vendor_id = row[0]
            vendor_name = row[1]
            labor_types = []

            if str_to_boolean(row[4]):
                labor_types.append(LaborType.UNION)
            if str_to_boolean(row[5]):
                labor_types.append(LaborType.NON_UNION)

            operating_systems = []
            if str_to_boolean(row[9]):
                operating_systems.append(OperatingSystem.MAC)
            if str_to_boolean(row[10]):
                operating_systems.append(OperatingSystem.PC)

            products = row[27].split(",")
            all_products.update(products)
            if row[26].split(",") == [""]:
                required_products = []
            else:
                required_products = row[26].split(",")

            target_customer_sizes = []

            for size in row[32].split(","):
                if size == "S":
                    target_customer_sizes.append(CompanySize.SMALL)
                elif size == "M":
                    target_customer_sizes.append(CompanySize.MEDIUM)
                elif size == "L":
                    target_customer_sizes.append(CompanySize.LARGE)

            itqd90 = int(row[30])
            vendor_ids_to_itqd90[vendor_id] = itqd90
            service_minimum_minutes = int(row[2])
            remote_only = str_to_boolean(row[7])

            vendor = Vendor(vendor_id, vendor_name, labor_types, cost=row[11], products=products, itq_d90=itqd90,
                            active_d90=row[31], operating_systems=operating_systems, remote_only=remote_only,
                            target_customer_sizes=target_customer_sizes, required_products=required_products,
                            no_small_jobs=row[6], service_minimum_minutes=service_minimum_minutes)

            vendors[vendor_id] = vendor

    return vendors, list(all_products), vendor_ids_to_itqd90

def generate_companies(num_companies):
    companies = dict()

    for i in range(num_companies):
        company = Company(i,
                          random.choice(CompanySize.CHOICES),
                          random.randrange(0, 4),
                          random.choice(LaborType.CHOICES),
                          )
        companies[i] = company

    return companies

def generate_orders(num_orders, num_companies, products):
    orders = dict()

    for i in range(num_orders):
        order = Order(i,
                      random.randrange(0, num_companies),
                      random.choice(products),
                      random.choice(OperatingSystem.CHOICES),
                      random.randrange(60, 300),
                      random.choices([True, False], [2, 8])
                      )
        orders[i] = order

    return orders

def simulate_matching(vendors, companies, orders):
    # for k, v in vendors.items():
    #     print(v)
    #
    # for k, v in companies.items():
    #     print(v)
    #
    # for k, v in orders.items():
    #     print(v)
    initial_matches = dict()

    for order_id, order in orders.items():
        for vendor_id, vendor in vendors.items():
            company = companies[order.company_id]
            if order.product in vendor.products \
                    and order.operating_system in vendor.operating_systems \
                    and company.labor_type in vendor.labor_types \
                    and company.size in vendor.target_customer_sizes \
                    and order.minimum_time_required > vendor.service_minimum_minutes:
                if order.on_site and not vendor.remote_only:
                    if order_id in initial_matches:
                        initial_matches[order_id].append(vendor_id)
                    else:
                        initial_matches[order_id] = [vendor_id]

    return initial_matches

def get_vendors_to_itq(matches, vendor_ids_to_itqd90):
    itqs = dict()

    for order_id, vendor_ids in matches.items():
        if len(vendor_ids) <= 3:
            itqs[order_id] = vendor_ids
        else:
            scored_vendors = score_vendors(vendor_ids, vendor_ids_to_itqd90)
            itqs[order_id] = scored_vendors

        for vendor_id in itqs[order_id]:
            vendor_ids_to_itqd90[vendor_id] = vendor_ids_to_itqd90[vendor_id] + 1

    return itqs

def score_vendors(vendor_ids, vendor_ids_to_itqd90):
    vendor_ids_to_itq = []
    h = []
    for vendor_id in vendor_ids:
        heappush(h, (vendor_ids_to_itqd90[vendor_id], vendor_id))

    # print(h)
    vendor_ids_to_itq.append(heappop(h)[1])
    vendor_ids_to_itq.append(heappop(h)[1])
    vendor_ids_to_itq.append(random.choice(h)[1])

    return vendor_ids_to_itq


def str_to_boolean(string):
    if string == "1":
        return True
    else:
        return False

if __name__ == "__main__":
    main()