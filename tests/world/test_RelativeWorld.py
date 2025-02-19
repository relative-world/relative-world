import unittest
from datetime import datetime, timedelta
from relative_world.world import RelativeWorld


class TestRelativeWorld(unittest.TestCase):
    """
    Test suite for the RelativeWorld class.
    """

    def setUp(self):
        """
        Set up the initial conditions for each test.
        """
        self.simulation_start_time = datetime(2023, 1, 1, 0, 0, 0)
        self.relative_world = RelativeWorld()
        self.relative_world.simulation_start_time = self.simulation_start_time

    def test_initial_time_step(self):
        """
        Test that the initial time_step is set to 15 minutes.
        """
        self.assertEqual(self.relative_world.time_step, timedelta(minutes=15))

    def test_update(self):
        """
        Test that the update method correctly advances the simulation time by one time_step.
        """
        self.relative_world.previous_iterations = 1
        self.relative_world.update()
        expected_time = self.simulation_start_time + timedelta(minutes=15)
        self.assertEqual(
            self.relative_world.simulation_start_time
            + self.relative_world.time_step * self.relative_world.previous_iterations,
            expected_time,
        )

    def test_update_without_start_time(self):
        """
        Test that updating without a start time raises a TypeError.
        """
        self.relative_world.simulation_start_time = None
        with self.assertRaises(TypeError):
            next(self.relative_world.update())

    def test_update_with_zero_time_step(self):
        """
        Test that updating with a zero time step does not change the simulation time.
        """
        self.relative_world.time_step = timedelta(0)
        self.relative_world.previous_iterations = 1
        list(self.relative_world.update())
        expected_time = self.simulation_start_time
        self.assertEqual(
            self.relative_world.simulation_start_time
            + self.relative_world.time_step * self.relative_world.previous_iterations,
            expected_time,
        )

    def test_update_with_negative_time_step(self):
        """
        Test that updating with a negative time step correctly adjusts the simulation time backward.
        """
        self.relative_world.time_step = timedelta(minutes=-15)
        list(self.relative_world.update())
        expected_time = self.simulation_start_time + timedelta(minutes=-15)
        self.assertEqual(
            self.relative_world.simulation_start_time
            + self.relative_world.time_step * self.relative_world.previous_iterations,
            expected_time,
        )


if __name__ == "__main__":
    unittest.main()
