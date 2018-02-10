#
# See the documentation for more details on how this works
#
# The idea here is you provide a simulation object that overrides specific
# pieces of WPILib, and modifies motors/sensors accordingly depending on the
# state of the simulation. An example of this would be measuring a motor
# moving for a set period of time, and then changing a limit switch to turn
# on after that period of time. This can help you do more complex simulations
# of your robot code without too much extra effort.
#
# NOTE: THIS API IS ALPHA AND WILL MOST LIKELY CHANGE!
#       ... if you have better ideas on how to implement, submit a patch!
#

from pyfrc.physics import drivetrains


class PhysicsEngine(object):
    '''
        Simulates a motor moving something that strikes two limit switches,
        one on each end of the track. Obviously, this is not particularly
        realistic, but it's good enough to illustrate the point
    '''

    def __init__(self, physics_controller):
        '''
            :param physics_controller: `pyfrc.physics.core.PhysicsInterface`
                                        object to communicate simulation
                                        effects to
        '''

        self.physics_controller = physics_controller
        self.position = 0

        self.physics_controller.add_analog_gyro_channel(1)

    def update_sim(self, hal_data, now, tm_diff):
        '''
            Called when the simulation parameters for the program need to be
            updated.

            :param now: The current time as a float
            :param tm_diff: The amount of time that has passed since the last
                            time that this function was called
        '''

        # Simulate the drivetrain
        l_talon = hal_data['CAN'][1]
        r_talon = hal_data['CAN'][3]

        speed, rotation = drivetrains.two_motor_drivetrain(
            l_talon['value'] , r_talon['value'] )
        self.physics_controller.drive(speed, rotation, tm_diff)

        # update position (use tm_diff so the rate is constant)
