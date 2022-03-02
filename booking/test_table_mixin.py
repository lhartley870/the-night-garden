import datetime
from datetime import date, timedelta, time
from itertools import chain
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Table, TimeSlot, Booking
from .views import TableSelectionMixin


class TestTableSelectionMixin(TestCase):

    # Set up test users, tables and time_slots.
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='usertest',
            password='123',
            email='usertest@gmail.com',
            first_name='Joe',
            last_name='Bloggs',
        )

        self.table1 = Table.objects.create(
            name='rose',
            size=2
        )

        self.table2 = Table.objects.create(
            name='lily',
            size=4
        )

        self.table3 = Table.objects.create(
            name='freesia',
            size=2
        )

        self.table4 = Table.objects.create(
            name='orchid',
            size=2
        )

        self.table5 = Table.objects.create(
            name='tulip',
            size=6
        )

        self.table6 = Table.objects.create(
            name='primrose',
            size=2
        )

        self.table7 = Table.objects.create(
            name='dahlia',
            size=2
        )

        self.table8 = Table.objects.create(
            name='poppy',
            size=4
        )

        self.table9 = Table.objects.create(
            name='violet',
            size=8
        )

        self.time_now = datetime.datetime.now()
        self.three_hours_forward = self.time_now + timedelta(hours=3)
        self.time_slot3 = TimeSlot.objects.create(
            time=time(
                self.three_hours_forward.hour,
                self.three_hours_forward.minute
            )
        )

        self.today = date.today()

    # Test TableSelectionMixin - only 1 table available to book.
    def test_one_table_available(self):
        self.time_slot3.tables.add(self.table5)
        self.client.login(username='usertest', password='123')
        self.client.post(
            reverse('make_booking'),
            data={
                'date': self.today + timedelta(days=20),
                'party_size': 2,
                'time_slot': self.time_slot3.id
            }
        )
        created_booking = Booking.objects.filter(
            booker=self.user1
        ).order_by(
            'created_on'
        ).last()
        booking_table = created_booking.tables.all()
        table5 = Table.objects.filter(id=self.table5.id)
        self.assertQuerysetEqual(
            booking_table,
            table5,
            transform=lambda x: x
        )

    # Test TableSelectionMixin - only 1 exact match table available to book -
    # expect that table to be allocated to the booking.
    def test_one_match_table_available(self):
        self.time_slot3.tables.add(self.table1, self.table5)
        self.client.login(username='usertest', password='123')
        self.client.post(
            reverse('make_booking'),
            data={
                'date': self.today + timedelta(days=20),
                'party_size': 2,
                'time_slot': self.time_slot3.id
            }
        )
        created_booking = Booking.objects.filter(
            booker=self.user1
        ).order_by(
            'created_on'
        ).last()
        booking_table = created_booking.tables.all()
        table1 = Table.objects.filter(id=self.table1.id)
        self.assertQuerysetEqual(
            booking_table,
            table1,
            transform=lambda x: x
        )

    # Test TableSelectionMixin - 2 exact match tables available to book,
    # expect one of those 2 tables to be allocated to the booking.
    def test_two_match_tables_available(self):
        self.time_slot3.tables.add(self.table1, self.table3)
        self.client.login(username='usertest', password='123')
        self.client.post(
            reverse('make_booking'),
            data={
                'date': self.today + timedelta(days=20),
                'party_size': 2,
                'time_slot': self.time_slot3.id
            }
        )
        created_booking = Booking.objects.filter(
            booker=self.user1
        ).order_by(
            'created_on'
        ).last()
        booking_table = created_booking.tables.all()
        tables_1_and_3 = [
            str(Table.objects.filter(id=self.table1.id)),
            str(Table.objects.filter(id=self.table3.id))
        ]
        self.assertIn(
            str(booking_table),
            tables_1_and_3,
        )

    # Test TableSelectionMixin - no exact match tables available to book,
    # all tables are larger than the party_size - only 1 table with the
    # smallest size of the available tables - expect that smallest size
    # table to be allocated to the booking.
    def test_all_larger_tables_one_smallest_available(self):
        self.time_slot3.tables.add(self.table5, self.table8, self.table9)
        self.client.login(username='usertest', password='123')
        self.client.post(
            reverse('make_booking'),
            data={
                'date': self.today + timedelta(days=20),
                'party_size': 2,
                'time_slot': self.time_slot3.id
            }
        )
        created_booking = Booking.objects.filter(
            booker=self.user1
        ).order_by(
            'created_on'
        ).last()
        booking_table = created_booking.tables.all()
        table8 = Table.objects.filter(id=self.table8.id)
        self.assertQuerysetEqual(
            booking_table,
            table8,
            transform=lambda x: x
        )

    # Test TableSelectionMixin - no exact match tables available to book,
    # all tables are larger than the party_size - 2 tables with the same
    # smallest size of the available tables - expect one of those 2 smallest
    # size tables to be allocated to the booking.
    def test_all_larger_tables_two_smallest_available(self):
        self.time_slot3.tables.add(self.table2, self.table8, self.table9)
        self.client.login(username='usertest', password='123')
        self.client.post(
            reverse('make_booking'),
            data={
                'date': self.today + timedelta(days=20),
                'party_size': 2,
                'time_slot': self.time_slot3.id
            }
        )
        created_booking = Booking.objects.filter(
            booker=self.user1
        ).order_by(
            'created_on'
        ).last()
        booking_table = created_booking.tables.all()
        tables_2_and_8 = [
            str(Table.objects.filter(id=self.table2.id)),
            str(Table.objects.filter(id=self.table8.id))
        ]
        self.assertIn(
            str(booking_table),
            tables_2_and_8,
        )

    # Test TableSelectionMixin - no exact match tables available to book,
    # all tables are smaller than the party_size - all tables are needed
    # for the booking - expect all tables to be allocated to the booking.
    def test_all_smaller_tables_all_needed(self):
        self.time_slot3.tables.add(
            self.table1,
            self.table2,
            self.table3,
            self.table4
        )
        self.client.login(username='usertest', password='123')
        self.client.post(
            reverse('make_booking'),
            data={
                'date': self.today + timedelta(days=20),
                'party_size': 9,
                'time_slot': self.time_slot3.id
            }
        )
        created_booking = Booking.objects.filter(
            booker=self.user1
        ).order_by(
            'created_on'
        ).last()
        booking_tables = created_booking.tables.all()
        all_timeslot_3_tables = self.time_slot3.tables.all()
        self.assertQuerysetEqual(
            booking_tables,
            all_timeslot_3_tables,
            transform=lambda x: x
        )

    # Test TableSelectionMixin - no exact match tables available to book,
    # all tables are smaller than the party_size - only 2 tables available
    # - expect both tables to be allocated to the booking.
    def test_all_smaller_tables_only_2_available(self):
        self.time_slot3.tables.add(self.table2, self.table5)
        self.client.login(username='usertest', password='123')
        self.client.post(
            reverse('make_booking'),
            data={
                'date': self.today + timedelta(days=20),
                'party_size': 7,
                'time_slot': self.time_slot3.id
            }
        )
        created_booking = Booking.objects.filter(
            booker=self.user1
        ).order_by(
            'created_on'
        ).last()
        booking_tables = created_booking.tables.all()
        all_timeslot_3_tables = self.time_slot3.tables.all()
        self.assertQuerysetEqual(
            booking_tables,
            all_timeslot_3_tables,
            transform=lambda x: x
        )

    # Test TableSelectionMixin - no exact match tables available to book,
    # all tables are smaller than the party_size - all tables are the same
    # size - expect the minumum number of tables needed to cover the
    # party_size to be allocated to the booking.
    def test_all_smaller_tables_same_size(self):
        self.time_slot3.tables.add(
            self.table1,
            self.table3,
            self.table4,
            self.table6
        )
        self.client.login(username='usertest', password='123')
        self.client.post(
            reverse('make_booking'),
            data={
                'date': self.today + timedelta(days=20),
                'party_size': 5,
                'time_slot': self.time_slot3.id
            }
        )
        created_booking = Booking.objects.filter(
            booker=self.user1
        ).order_by(
            'created_on'
        ).last()
        booking_tables = len(created_booking.tables.all())
        self.assertEqual(
            booking_tables,
            3
        )

    # Test TableSelectionMixin - no exact match tables available to book,
    # all tables are smaller than the party_size - there are more than 2
    # tables available, not all tables are the same size and not all tables
    # are needed to cover the party_size - there is 1 match combination
    # within the available tables - expect that match combination to be
    # allocated to the booking.
    def test_all_smaller_tables_1_match_combination(self):
        self.time_slot3.tables.add(self.table1, self.table2, self.table5)
        self.client.login(username='usertest', password='123')
        self.client.post(
            reverse('make_booking'),
            data={
                'date': self.today + timedelta(days=20),
                'party_size': 10,
                'time_slot': self.time_slot3.id
            }
        )
        created_booking = Booking.objects.filter(
            booker=self.user1
        ).order_by(
            'created_on'
        ).last()
        booking_tables = created_booking.tables.all()
        table2 = Table.objects.filter(id=self.table2.id)
        table5 = Table.objects.filter(id=self.table5.id)
        table2_and_table5 = list(chain(table2, table5))
        self.assertQuerysetEqual(
            booking_tables,
            table2_and_table5,
            transform=lambda x: x
        )

    # Test TableSelectionMixin - no exact match tables available to book,
    # all tables are smaller than the party_size - there are more than 2 tables
    # available, not all tables are the same size and not all tables are needed
    # to cover the party_size - there is more than 1 match combination
    # within the available tables but only 1 match combination with the
    # smallest number of tables - expect the match combination with the
    # smallest number of tables to be allocated to the booking.
    def test_all_smaller_tables_match_combo_smallest_num_tables(self):
        self.time_slot3.tables.add(
            self.table1,
            self.table2,
            self.table3,
            self.table4,
            self.table5
        )
        self.client.login(username='usertest', password='123')
        self.client.post(
            reverse('make_booking'),
            data={
                'date': self.today + timedelta(days=20),
                'party_size': 9,
                'time_slot': self.time_slot3.id
            }
        )
        created_booking = Booking.objects.filter(
            booker=self.user1
        ).order_by(
            'created_on'
        ).last()
        booking_tables = created_booking.tables.all()
        table2 = Table.objects.filter(id=self.table2.id)
        table5 = Table.objects.filter(id=self.table5.id)
        table2_and_table5 = list(chain(table2, table5))
        self.assertQuerysetEqual(
            booking_tables,
            table2_and_table5,
            transform=lambda x: x
        )

    # Test TableSelectionMixin - no exact match tables available to
    # book, all tables are smaller than the party_size - there are more
    # than 2 tables available, not all tables are the same size and not
    # all tables are needed to cover the party_size - there is more than
    # 1 match combination within the available tables and more than 1 match
    # combination with the smallest number of tables - and both of those
    # combinations have the same largest table size -  expect one of the
    # match combinations with the smallest number of tables to be allocated
    # to the booking.
    def test_smaller_tables_match_combo_smallest_num_tables_same_largest(self):
        self.time_slot3.tables.add(
            self.table1,
            self.table2,
            self.table3,
            self.table4,
            self.table5,
            self.table9
        )
        self.client.login(username='usertest', password='123')
        self.client.post(
            reverse('make_booking'),
            data={
                'date': self.today + timedelta(days=20),
                'party_size': 9,
                'time_slot': self.time_slot3.id
            }
        )
        created_booking = Booking.objects.filter(
            booker=self.user1
        ).order_by(
            'created_on'
        ).last()
        booking_tables = created_booking.tables.all()
        table1 = Table.objects.filter(id=self.table1.id)
        table3 = Table.objects.filter(id=self.table3.id)
        table4 = Table.objects.filter(id=self.table4.id)
        table9 = Table.objects.filter(id=self.table9.id)
        tables_1_and_9 = list(chain(table1, table9))
        tables_3_and_9 = list(chain(table3, table9))
        tables_4_and_9 = list(chain(table4, table9))
        all_table_combinations = [
            f'<QuerySet {tables_1_and_9}>',
            f'<QuerySet {tables_3_and_9}>',
            f'<QuerySet {tables_4_and_9}>'
        ]
        self.assertIn(
            str(booking_tables),
            all_table_combinations,
        )

    # Test TableSelectionMixin - no exact match tables available to book,
    # all tables are smaller than the party_size - there are more than 2 tables
    # available, not all tables are the same size and not all tables are needed
    # to cover the party_size - there is more than 1 match combination within
    # the available tables and more than 1 match combination with the smallest
    # number of tables - expect the match combinations containing the largest
    # table size to be allocated to the booking.
    def test_smaller_tables_match_combo_smallest_num_tables_largest_size(self):
        self.time_slot3.tables.add(
            self.table2,
            self.table4,
            self.table5,
            self.table9
        )
        self.client.login(username='usertest', password='123')
        self.client.post(
            reverse('make_booking'),
            data={
                'date': self.today + timedelta(days=20),
                'party_size': 9,
                'time_slot': self.time_slot3.id
            }
        )
        created_booking = Booking.objects.filter(
            booker=self.user1
        ).order_by(
            'created_on'
        ).last()
        booking_tables = created_booking.tables.all()
        table4 = Table.objects.filter(id=self.table4.id)
        table9 = Table.objects.filter(id=self.table9.id)
        table4_and_table9 = list(chain(table4, table9))
        self.assertQuerysetEqual(
            booking_tables,
            table4_and_table9,
            transform=lambda x: x
        )

    # Test TableSelectionMixin - no exact match tables available to book,
    # all tables are smaller than the party_size - there are more than 2 tables
    # available, not all tables are the same size and not all tables are needed
    # to cover the party_size - there is more than 1 match combination within
    # the available tables, more than 1 match combination with the smallest
    # number of tables and more than 1 match combination containing the largest
    # size table - expect one of the match combinations containing the largest
    # size table to be allocated to the booking.
    def test_smaller_tables_match_combo_smallest_num_tables_two_largest(self):
        self.time_slot3.tables.add(
            self.table1,
            self.table2,
            self.table4,
            self.table5,
            self.table9
        )
        self.client.login(username='usertest', password='123')
        self.client.post(
            reverse('make_booking'),
            data={
                'date': self.today + timedelta(days=20),
                'party_size': 9,
                'time_slot': self.time_slot3.id
            }
        )
        created_booking = Booking.objects.filter(
            booker=self.user1
        ).order_by(
            'created_on'
        ).last()
        booking_tables = created_booking.tables.all()
        table1 = Table.objects.filter(id=self.table1.id)
        table4 = Table.objects.filter(id=self.table4.id)
        table9 = Table.objects.filter(id=self.table9.id)
        tables_1_and_9 = list(chain(table1, table9))
        tables_4_and_9 = list(chain(table4, table9))
        all_table_combinations = [
            f'<QuerySet {tables_1_and_9}>',
            f'<QuerySet {tables_4_and_9}>'
        ]
        self.assertIn(
            str(booking_tables),
            all_table_combinations,
        )

    # Test TableSelectionMixin - no exact match tables available to book,
    # some tables are smaller and some are larger than the party_size -
    # there are no match combinations of tables - there is only 1
    # table/combination with the smallest capacity greater than the
    # party_size - expect that table/combination of tables to be allocated
    # to the booking.
    def test_mixed_tables_no_match_combo_one_combo_min_capacity(self):
        self.time_slot3.tables.add(self.table1, self.table4, self.table9)
        self.client.login(username='usertest', password='123')
        self.client.post(
            reverse('make_booking'),
            data={
                'date': self.today + timedelta(days=20),
                'party_size': 5,
                'time_slot': self.time_slot3.id
            }
        )
        created_booking = Booking.objects.filter(
            booker=self.user1
        ).order_by(
            'created_on'
        ).last()
        booking_tables = created_booking.tables.all()
        table9 = Table.objects.filter(id=self.table9.id)
        self.assertQuerysetEqual(
            booking_tables,
            table9,
            transform=lambda x: x
        )

    # Test TableSelectionMixin - no exact match tables available to book,
    # some tables are smaller and some are larger than the party_size -
    # there are no match combinations of tables - there is more than 1
    # table/combination with the smallest capacity greater than the party_size
    # - of those there is only 1 table/combination with the smallest number of
    # tables - expect that table/combination of tables to be allocated to
    # the booking.
    def test_mixed_tables_no_match_combo_two_combo_min_capacity_sm_num(self):
        self.table10 = Table.objects.create(
            name='daffodil',
            size=10
        )
        self.time_slot3.tables.add(self.table5, self.table8, self.table10)
        self.client.login(username='usertest', password='123')
        self.client.post(
            reverse('make_booking'),
            data={
                'date': self.today + timedelta(days=20),
                'party_size': 7,
                'time_slot': self.time_slot3.id
            }
        )
        created_booking = Booking.objects.filter(
            booker=self.user1
        ).order_by(
            'created_on'
        ).last()
        booking_tables = created_booking.tables.all()
        table10 = Table.objects.filter(id=self.table10.id)
        self.assertQuerysetEqual(
            booking_tables,
            table10,
            transform=lambda x: x
        )

    # Test TableSelectionMixin - no exact match tables available to book,
    # some tables are smaller and some are larger than the party_size -
    # there are no match combinations of tables - there is more than 1
    # table/combination with the smallest capacity greater than the party_size
    # - of those there are 2 tables/combinations with the smallest number of
    # tables - expect one of those tables/combinations of tables to be
    # allocated to the booking.
    def test_mixed_tables_no_match_combo_two_combo_min_capacity_2_sm_num(self):
        self.table10 = Table.objects.create(
            name='daffodil',
            size=10
        )
        self.table11 = Table.objects.create(
            name='hyacinth',
            size=10
        )
        self.time_slot3.tables.add(
            self.table5,
            self.table8,
            self.table10,
            self.table11
        )
        self.client.login(username='usertest', password='123')
        self.client.post(
            reverse('make_booking'),
            data={
                'date': self.today + timedelta(days=20),
                'party_size': 7,
                'time_slot': self.time_slot3.id
            }
        )
        created_booking = Booking.objects.filter(
            booker=self.user1
        ).order_by(
            'created_on'
        ).last()
        booking_table = created_booking.tables.all()
        tables_10_and_11 = [
            str(Table.objects.filter(id=self.table10.id)),
            str(Table.objects.filter(id=self.table11.id))
        ]
        self.assertIn(
            str(booking_table),
            tables_10_and_11,
        )

    # Test TableSelectionMixin select_tables method where there are
    # no available tables.
    def test_tableselectionmixin_select_tables_returns_none(self):
        mixin = TableSelectionMixin()
        result = mixin.select_tables(available_tables=[], party_size=2)
        self.assertEqual(result, None)
