class Colors:
    dark_grey = '#52556b'
    green = '#14ba41'
    blue = '#227ade'
    red = '#e43d47'
    orange = '#d18624'
    pink = '#c217ae'
    violet = '#5f109c'
    yellow = '#f9dc0f'
    white = '#f1f1ee'
    light_green = '#29d388'

    # We inherit the method from the Grid class
    @classmethod
    def get_cell_colors(cls):
        return [cls.dark_grey, cls.green, cls.blue, cls.red, cls.orange, cls.pink,
                cls.violet, cls.yellow]  # Add 'cls' to get color values
