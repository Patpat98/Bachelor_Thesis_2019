import numpy as np
import matplotlib.pyplot as plt

import os
import sys
sys.path.insert(0, '\\'.join(os.getcwd().split('\\')[:-1]) + '\\tools')

from GoogleSheetsImport import GoogleSheetsDataImport, SHEET_NAMES, SPREADSHEET_ID


class CgCalculation(object):

    def __init__(self, components: dict):
        """
        Object to calculate the centre of gravity in 3 Dimensions for any system
        :param components: {
                    component: (weight, (x, z)),
                    ...
                    }
        """

        self.__components = components
        self.__cg = [None, None]
        self.__cg_lemac = [None, None]
        self.calculate_cg()
        # self.cg_xlemac()

    def add_component(self, name: str, weight: float, position: tuple):
        """
        Add Component to the calculation
        :param name: Component Name
        :param weight: Component Weight
        :param position: Component position in (x, z)
        :return:
        """

        self.__components[name] = (weight, position)
        self.calculate_cg()

    @staticmethod
    def __calculate_cg_along_x(components: dict):
        """
        Calculate X coordinate of CG
        :return:
        """
        return sum([weight * position[0] for name, (weight, position) in components.items()])\
               / sum([weight for name, (weight, position) in components.items()])

    @staticmethod
    def __calculate_cg_along_z(components: dict):
        """
        Calculate Z coordinate of CG
        :return:
        """
        return sum([weight * position[1] for name, (weight, position) in components.items()])\
               / sum([weight for name, (weight, position) in components.items()])

    def calculate_cg(self):
        """
        Calculate x, z position of CG
        :return:
        """
        self.__cg = [self.__calculate_cg_along_x(self.__components), self.__calculate_cg_along_z(self.__components)]
        return self.__cg

    def cg_xlemac(self, d_xlemac: float):
        """
        Calculate CG in XLEMAC coordinates
        :param d_xlemac: Distance from nose tip to XLEMAC
        :return:
        """
        self.__cg_lemac = [self.__cg[0] - d_xlemac, self.__cg[1]]
        return self.__cg_lemac

    @staticmethod
    def __plot_cilinder(length: float, height: float, offset: tuple = (0, 0)):

        height = height/2
        xdata = []
        ydata = []

        # First Circular Part
        for theta in np.linspace(0, np.pi/2, 10):
            xdata.append(height - np.cos(theta)*height)
            ydata.append(np.sin(theta)*height)

        # Straight Part
        for xi in np.linspace(height, length-height, 100):
            xdata.append(xi)
            ydata.append(height)

        # Second Circular Part
        for theta in np.linspace(np.pi/2, 0, 10):
            xdata.append(length - height + np.cos(theta)*height)
            ydata.append(np.sin(theta)*height)

        bottom_x = []
        bottom_y = []

        for xi, yi in zip(xdata[::-1], ydata[::-1]):
            bottom_x.append(xi)
            bottom_y.append(-yi)

        xdata.extend(bottom_x)
        ydata.extend(bottom_y)

        return np.array(xdata) + offset[0], np.array(ydata) + offset[1]

    def wing_positioning_plot(self, fig=None):
        """
        Wing Positioning
        :return:
        """

        data = GoogleSheetsDataImport(SPREADSHEET_ID, *SHEET_NAMES)
        data.coordinate_transform()
        data = data.get_data()
        fuselage = data['Structures']['Max_fuselage_length']
        chord = data['Aero']['Wing chord']

        if fig is None:
            fig = plt.figure()

        wing_weight = self.__components['Wing'][0]
        wing_pos = self.__components['Wing'][1]
        components = dict(self.__components)

        empty_cgs = []

        for xwing in np.linspace(0.2, 0.7):
            components['Wing'] = (wing_weight, (xwing*fuselage - chord/2, wing_pos[1]))
            components['Payload'] = (0,(0,0))
            cg = (self.__calculate_cg_along_x(components) - xwing*fuselage)/chord
            empty_cgs.append(cg)

        empty_cgs = np.array(empty_cgs)

        full_cgs = []
        components = dict(self.__components)

        for xwing in np.linspace(0.2, 0.7):
            components['Wing'] = (wing_weight, (xwing*fuselage - chord/2, wing_pos[1]))
            cg = (self.__calculate_cg_along_x(components) - xwing*fuselage)/chord
            full_cgs.append(cg)

        full_cgs = np.array(full_cgs)

        plt.plot(empty_cgs, np.linspace(0.2, 0.7), 'r-', label='Empty Payload')
        plt.plot(full_cgs, np.linspace(0.2, 0.7), 'b-', label='Full Payload')
        plt.grid()
        plt.legend()
        plt.xlabel('$x_{cg}/MAC$')
        plt.ylabel('$x_{LEMAC}/l_{fus}$')
        plt.title(f'Payload @ {round(components["Payload"][1][0]/fuselage, 2)}')

    def plot_locations(self, fig: plt.figure = None):
        """
        Make a component plot of all components and weights
        :param fig: fig to plot in
        :return:
        """

        if fig is None:
            fig, ax = plt.subplots()
            ax.set_aspect(1.0)
            plt.xlim(0, 15)
            plt.ylim(0, 15)

        coordinate_history = []
        for name, (weight, (x, z)) in self.__components.items():
            i = 1
            if (x, z) in coordinate_history:
                i = 3
            plt.scatter(x, z, s=np.sqrt(weight), c='k')
            plt.annotate(name, xy=(x+i*0.1, z+i*0.1))
            coordinate_history.append((x,z))
        plt.scatter(self.__cg[0], self.__cg[1], c='r')
        plt.annotate('CG', xy=self.__cg)

        # fuselage = self.__plot_cilinder(9, 2.5)
        # wing = self.__plot_cilinder(2.25, 0.5, offset=(3, 1.5))
        #
        # plt.plot(fuselage[0], fuselage[1], 'k-')
        # plt.plot(wing[0], wing[1], 'k-')

        plt.grid()
        plt.xlabel('X Position [m]')
        plt.ylabel('Y Position [m]')
        plt.title('CG Location')


if __name__ == '__main__':

    data = GoogleSheetsDataImport(SPREADSHEET_ID, *SHEET_NAMES).get_data()

    components = {
        'Fuselage': (data['Structures']['Fuselage_weight [N]'], data['C&S']['Fuselage']),
        'Wing': (data['Structures']['Wing_weight [N]'], data['C&S']['Wing']),
        'Engine': (data['FPP']['Engine Weight [N]'], data['C&S']['Engine']),
        'Horizontal Tail': (data['Structures']['HTail_weight [N]'], data['C&S']['H Wing']),
        'Vertical Tail': (data['Structures']['VTail_weight [N]'], data['C&S']['V Wing']),
        'Payload': (data['Weights']['WPL [N]'], data['C&S']['Payload']),
        'Fuel': (data['Weights']['WF [N]'], data['C&S']['Wing'])
    }

    B = CgCalculation(components)
    B.plot_locations()
    print("CG: ", B.calculate_cg())
    B.wing_positioning_plot()
