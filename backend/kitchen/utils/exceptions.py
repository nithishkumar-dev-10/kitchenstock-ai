class KitchenBaseError(Exception):
    """Base class for all kitchen exceptions"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ItemNotFoundError(KitchenBaseError):
    """Raised when an inventory item or dish does not exist"""
    pass


class InvalidInputError(KitchenBaseError):
    """Raised when input values are invalid (e.g. quantity <= 0)"""
    pass


class InsufficientStockError(KitchenBaseError):
    """Raised when there isn't enough stock to cook a dish"""
    pass


class DataLoadError(KitchenBaseError):
    """Raised when a JSON data file cannot be loaded"""
    pass


class NoDataAvailableError(KitchenBaseError):
    """Raised when a dataset is empty (no dishes, no inventory)"""
    pass