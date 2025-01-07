class Singleton(type):
    """
    Singleton is a metaclass that ensures only one instance of any class
    with this metaclass can exist.

    It overrides the __call__ method to check if an instance already exists
    for the class. If it does, it returns the existing instance. If it doesn't,
    it creates a new one.

    Attributes:
        _instances (dict): A dictionary to hold the instances of the classes.
                           The keys are the classes and the values are the instances.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Overrides the __call__ method to ensure only one instance of the class exists.

        If an instance of the class already exists, it returns the existing instance.
        If an instance does not exist, it creates a new one and stores it in the _instances dictionary.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            object: The instance of the class.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
