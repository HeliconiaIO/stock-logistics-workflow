from odoo.tests.common import TransactionCase


class TestStockMoveLine(TransactionCase):
    def setUp(self):
        super().setUp()
        # Set up required records for the test
        self.product = self.env["product.product"].create(
            {
                "name": "Test Product",
                "sale_line_warn": "no-message",
            }
        )
        self.stock_location = self.env["stock.location"].create(
            {
                "name": "Test Location",
            }
        )
        self.picking_type = self.env["stock.picking.type"].create(
            {"name": "Test Picking Type", "code": "outgoing", "sequence_code": "SPT"}
        )
        self.picking = self.env["stock.picking"].create(
            {
                "picking_type_id": self.picking_type.id,
                "location_id": self.stock_location.id,
                "location_dest_id": self.stock_location.id,
            }
        )
        self.move = self.env["stock.move"].create(
            {
                "name": "Test Move",
                "product_id": self.product.id,
                "product_uom_qty": 10,
                "location_id": self.stock_location.id,
                "location_dest_id": self.stock_location.id,
                "picking_id": self.picking.id,
            }
        )
        self.move_line = self.env["stock.move.line"].create(
            {
                "product_id": self.product.id,
                "move_id": self.move.id,
                "location_id": self.stock_location.id,
                "location_dest_id": self.stock_location.id,
            }
        )

    def test_linked_reference_with_picking(self):
        self.assertEqual(
            self.move_line.linked_reference,
            self.picking,
            "linked_reference should point to the picking when available",
        )

    def test_linked_reference_with_move(self):
        self.move.picking_id = False
        self.move_line._compute_linked_reference()
        self.assertEqual(
            self.move_line.linked_reference,
            self.move,
            "linked_reference should point to the move when picking is not available",
        )

    def test_linked_reference_no_reference(self):
        # Detach move reference entirely and test
        self.move_line.move_id = False
        self.move_line._compute_linked_reference()  # Trigger compute manually
        self.assertFalse(
            self.move_line.linked_reference,
            "linked_reference should be False if no picking or move is available",
        )
