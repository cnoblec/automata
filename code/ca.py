import numpy





def arrayIndexes(shape):
    
    
    """
    arrayIndexes                                                Python Documentation
    
    Indexes of an N-Dimensional Array
    
    
    
    Description:
    
    Get the index of each element of an n-dimensional array. Each index is returned
    as a tuple of integers, with the last dimension being iterated over fastest.
    
    
    
    Usage:
    
    arrayIndexes(shape)
    
    
    
    Arguments:
    
    shape
    
        a tuple of integers; the shape of an n-dimensional array.
    
    
    
    Value:
    
    A list of tuples of integers. The list will contain 'numpy.prod(shape)' tuples
    and each tuple will contain 'len(shape)' integers.
    
    
    
    Note:
    
    This function has similar behaviour to 'list(numpy.ndindex(shape))'. The
    difference is that 'arrayIndexes' uses negative integers for the second half of
    each dimension.
    
    
    
    Examples:
    
    arrayIndexes( (4, 5) )
    """
    
    
##    x = [numpy.arange(n) for n in shape]
    
    
    # similar to the above code, but uses a split of positive and negative indexes
    x = [numpy.concatenate((
        numpy.arange(0,  (n + 1)//2),
        numpy.arange(-(n - 1)//2, 0)
    )) for n in shape]
    
    
    # each element of the above arrays must be repeated 'each' times
    each = numpy.cumprod((1,) + shape[:0:-1])[::-1]
    
    
    # after repeating the array with 'each',
    # the entire array must be repeated 'times' times
    times = numpy.prod(shape)//(shape * each)
    return list(zip(*[
        numpy.concatenate([x_.repeat(each_)] * times_) for x_, each_, times_ in zip(
            x, each, times
        )
    ]))





NEIGHBOURS = numpy.array([
    
    
    # 1D neighbours
    numpy.array([
        [(NEIGHBOURS1D2OP := 0), (lambda indx : [
                                      (indx[0] + 1,),  # right 1
                                      (indx[0] - 1,)   # left  1
                                  ])
        ]
    ], dtype = object),
    
    
    # 2D neighbours
    numpy.array([
        [(NEIGHBOURS2D4OP := 1), (lambda indx : [
                                      (indx[0]    , indx[1] + 1),  # right 1
                                      (indx[0] - 1, indx[1]    ),  # up    1
                                      (indx[0]    , indx[1] - 1),  # left  1
                                      (indx[0] + 1, indx[1]    )   # down  1
                                  ])
        ],
        [(NEIGHBOURS2D8OP := 2), (lambda indx : [
                                      (indx[0]    , indx[1] + 1),  # right 1
                                      (indx[0] - 1, indx[1] + 1),  # right 1 up   1
                                      (indx[0] - 1, indx[1]    ),  #         up   1
                                      (indx[0] - 1, indx[1] - 1),  # left  1 up   1
                                      (indx[0]    , indx[1] - 1),  # left  1
                                      (indx[0] + 1, indx[1] - 1),  # left  1 down 1
                                      (indx[0] + 1, indx[1]    ),  #         down 1
                                      (indx[0] + 1, indx[1] + 1)   # right 1 down 1
                                  ])
        ]
    ], dtype = object),

    numpy.array([
        [(NEIGHBOURS3DOPVN := 3),   (lambda indx : [
                                    (indx[0]    , indx[1]    , indx[2] + 1),  # x + 1 , y     , z
                                    (indx[0]    , indx[1]    , indx[2] - 1),  # x - 1 , y     , z
                                    (indx[0]    , indx[1] + 1, indx[2]    ),  # x     , y + 1 , z
                                    (indx[0]    , indx[1] - 1, indx[2]    ),  # x     , y - 1 , z
                                    (indx[0] + 1, indx[1]    , indx[2]    ),  # x     , y     , z + 1
                                    (indx[0] - 1, indx[1]    , indx[2]    ),  # x     , y     , z - 1
                                  ])
        ],
        [(NEIGHBOURS3DOPMOORE := 4),    (lambda indx : [
                                        (indx[0]    , indx[1]    , indx[2] + 1),  # x + 1 , y     , z
                                        (indx[0]    , indx[1] + 1, indx[2] + 1),  # x + 1 , y + 1 , z
                                        (indx[0]    , indx[1] - 1, indx[2] + 1),  # x + 1 , y - 1 , z
                                        (indx[0] + 1, indx[1]    , indx[2] + 1),  # x + 1 , y     , z + 1
                                        (indx[0] - 1, indx[1]    , indx[2] + 1),  # x + 1 , y     , z - 1
                                        (indx[0] + 1, indx[1] + 1, indx[2] + 1),  # x + 1 , y + 1 , z + 1
                                        (indx[0] - 1, indx[1] + 1, indx[2] + 1),  # x + 1 , y + 1 , z - 1
                                        (indx[0] + 1, indx[1] - 1, indx[2] + 1),  # x + 1 , y - 1 , z + 1
                                        (indx[0] - 1, indx[1] - 1, indx[2] + 1),  # x + 1 , y - 1 , z - 1
                                        (indx[0]    , indx[1]    , indx[2] - 1),  # x - 1 , y     , z
                                        (indx[0]    , indx[1] + 1, indx[2] - 1),  # x - 1 , y + 1 , z
                                        (indx[0]    , indx[1] - 1, indx[2] - 1),  # x - 1 , y - 1 , z
                                        (indx[0] + 1, indx[1]    , indx[2] - 1),  # x - 1 , y     , z
                                        (indx[0] - 1, indx[1]    , indx[2] - 1),  # x - 1 , y     , z
                                        (indx[0] + 1, indx[1] + 1, indx[2] - 1),  # x - 1 , y + 1 , z + 1
                                        (indx[0] - 1, indx[1] + 1, indx[2] - 1),  # x - 1 , y + 1 , z - 1
                                        (indx[0] + 1, indx[1] - 1, indx[2] - 1),  # x - 1 , y - 1 , z + 1
                                        (indx[0] - 1, indx[1] - 1, indx[2] - 1),  # x - 1 , y - 1 , z - 1                                        (indx[0]    , indx[1] + 1, indx[2]    ),  # x     , y + 1 , z
                                        (indx[0]    , indx[1] + 1, indx[2]    ),  # x     , y + 1 , z
                                        (indx[0]    , indx[1] - 1, indx[2]    ),  # x     , y - 1 , z
                                        (indx[0] + 1, indx[1] + 1, indx[2]    ),  # x     , y + 1 , z + 1
                                        (indx[0] - 1, indx[1] + 1, indx[2]    ),  # x     , y + 1 , z - 1
                                        (indx[0] + 1, indx[1] - 1, indx[2]    ),  # x     , y - 1 , z + 1
                                        (indx[0] - 1, indx[1] - 1, indx[2]    ),  # x     , y - 1 , z - 1
                                        (indx[0] + 1, indx[1]    , indx[2]    ),  # x     , y     , z + 1
                                        (indx[0] - 1, indx[1]    , indx[2]    ),  # x     , y     , z - 1
                                  ])
        ]
    ], dtype = object)
    
    
], dtype = object)
OPS_LIST =                   [x[:, 0].astype(int) for x in NEIGHBOURS]
OPS      = numpy.concatenate(OPS_LIST)
GETTERS  = numpy.concatenate([x[:, 1]             for x in NEIGHBOURS])
if not numpy.array_equal(OPS, range(len(OPS))):
    raise ValueError(f"invalid OPS, should be 0:{len(OPS)}")





class CA:
    
    
    def __init__(self, shape = None, cell_type = None, lattice = None,
        neighbour_order = None):
        
        
        """
        __init__                                                    Python Documentation
        
        Initialize an Object of Class "CA"
        
        
        
        Description:
        
        The constructor for class "CA" representing a lattice of cells.
        
        
        
        Usage:
        
        CA(shape = None, cell_type = None, lattice = None, neighbour_order = None)
        
        
        
        Arguments:
        
        shape
        
            integer or tuple of integers; the shape of the lattice.
        
        cell_type
        
            a type or a numpy.dtype; the class of the objects in the lattice.
        
        lattice
        
            an object of class numpy.ndarray; an alternative way to specify the state
            of the lattice.
        
        neighbour_order
        
            integer; how should the cells behave with their neighbouring cells?
        
        
        
        Details:
        
        You must provide either 'shape' or 'lattice', but not both.
        
        'cell_type' should be a type:
            int, float, str, object, etc.
        or a numpy.dtype:
            int32, float64, <U16, O, etc.
        """
        
        
        nargs = (shape is not None) + (lattice is not None)
        if nargs < 1:
            raise ValueError("provide either 'shape' or 'lattice'")
        if nargs > 1:
            raise ValueError("only one of 'shape' and 'lattice' can be used")
        which = "shape" if (shape is not None) else "lattice"
        
        
        if neighbour_order is None:
            op = None
        else:
            op = int(neighbour_order)
            if not (op in OPS):
                raise ValueError("invalid 'neighbour_order'")
        
        
        if shape is not None:
            if not (isinstance(cell_type, type       ) |
                    isinstance(cell_type, numpy.dtype)):
                raise ValueError("invalid 'cell_type' argument")
            lattice = numpy.empty(shape = shape, dtype = cell_type)
        else:
            if cell_type is None:
                lattice = numpy.asarray(lattice)
                cell_type = lattice.dtype
            else:
                if not (isinstance(cell_type, type       ) |
                        isinstance(cell_type, numpy.dtype)):
                    raise ValueError("invalid 'cell_type' argument")
                lattice = numpy.asarray(lattice, dtype = cell_type)
        if lattice.ndim <= 0:
            raise ValueError("invalid '{which}', cannot use 0 dimensional array for automata")
        if lattice.ndim > len(OPS_LIST):
            raise ValueError(f"invalid '{which}', {lattice.ndim} dimensional automata are not yet implemented")
        
        
        self.cell_type = cell_type
        self.lattice   = lattice
        
        
        if op is None:
            op = OPS_LIST[self.lattice.ndim - 1][0]
        else:
            if not (op in OPS_LIST[self.lattice.ndim - 1]):
                raise ValueError(f"invalid 'neighbour_order'")
        
        
        self.op      = op
        
        
        self.__neighbours = GETTERS[self.op]
        return
    
    
    def __len__(self):
        return self.lattice.size
    
    
    def empty(self):
        
        
        """
        empty                                                       Python Documentation
        
        Create a New, Empty Lattice
        
        
        
        Description:
        
        Create a new, empty lattice (a temp lattice), useful for evolving the state of
        a cellular automata.
        
        
        
        Usage:
        
        empty()



        Details:

        If the cellular automata has an attribute "fill_value", it will be used with
        'numpy.full' to create an empty lattice.
        
        Otherwise, if the cellular automata's lattice is boolean, integer, float, or
        complex typed, 'numpy.zeros' will be used to create an empty lattice.

        Otherwise, 'numpy.empty' will be used to create an empty lattice.
        
        
        
        Note:
        
        This method can be overridden as necessary by a subclass.
        """
        
        
        if hasattr(self, "fill_value"):
            return numpy.full (self.lattice.shape, self.fill_value, self.lattice.dtype)
        elif self.lattice.dtype in [bool, int, float, complex]:
            return numpy.zeros(self.lattice.shape, self.lattice.dtype)
        else:
            return numpy.empty(self.lattice.shape, self.lattice.dtype)
    
    
    def empty_fun(self):
        shape = self.lattice.shape
        dtype = self.lattice.dtype
        if hasattr(self, "fill_value"):
            fill_value = self.fill_value
            return lambda : numpy.full (shape, fill_value, dtype)
        elif self.lattice.dtype in [bool, int, float, complex]:
            return lambda : numpy.zeros(shape, dtype)
        else:
            return lambda : numpy.empty(shape, dtype)
    
    
    def items(self):
        return ( ("lattice", self.lattice) ,
##                 ("cell type", self.cell_type.__name__ if isinstance(self.cell_type, type) else cell_type.__class__.__name__) ,
                 ("dimensions", self.lattice.shape) )
    
    
    def __str__(self):
        value = f"An object of class \"{self.__class__.__name__}\"\n"
        for tag , item in self.items():
            value += f"\n{tag}:\n{item}\n"
        return value
    
    
    def __getitem__(self, indexes):
        return self.lattice[indexes]
    
    
    def __setitem__(self, indexes, value):
        return self.lattice.__setitem__(indexes, value)
    
    
    def neighbours(self, indx):
        
        
        """
        neighbours                                                  Python Documentation
        
        Get Indexes of Lattice Neighbours
        
        
        
        Description:
        
        Get a list of the indexes of the neighbouring cells.
        
        
        
        Usage:
        
        neighbours(indx)
        
        
        
        Arguments:
        
        indx
        
            integer; an index of the lattice. This function is intended to receive an
            index of a flat lattice and return the neighbouring cells flat indexes.
            This is mostly for convenience, it's annoying (but not impossible) to index an
            arbitrarily sized lattice, but very easy to index a 1D lattice.
        
        Value:
        
        A list of integers.
        """
        
        
        return self.__neighbours(indx)
    
    
    def no_update_method(self, which):
        raise NotImplementedError(
           f"object has no '{which}' method\n"
            "\n"
            "A CA subclass should define an 'update' and 'update_random' method which will\n"
            "update (deterministicly or randomly, respectively) an individual cell (and\n"
            "possibly its neighbouring cells).\n"
            "\n"
            "The 'update'        method should have a signature update(self, old, new, indx)\n"
            "The 'update_random' method should have a signature update_random(self, x, indx)\n"
            "\n"
            "'old' and 'new' are the old lattice (not to be updated) and the new lattice\n"
            "(the temp lattice to be update), respectively.\n"
            "\n"
            "'x' is the lattice being updated.\n"
            "\n"
            "'indx' is the index of the cell which should be updated (and possibly its\n"
            "neighbours).\n"
            "\n"
            "You will likely need the indexes of the neighbouring cells; they can be easily\n"
            "retrieved with 'self.neighbours(indx)'. The indexes of the neighbours are not\n"
            "included in the signature in the event that they are not needed. It would be a\n"
            "waste of time to calculate them if they aren't going to be made use of.\n"
            "\n"
            "Both methods should return None, though it isn't an issue if it doesn't.\n"
            "The return value is not made use of."
        )
    
    
    def update(self, old, new, indx):
        self.no_update_method("update")
        return
    
    
    def update_random(self, x, indx):
        self.no_update_method("update_random")
        return
    
    
    def evolve(self, updates_per_cell = 1):
        
        
        n_cells = len(self)
        
        
        updates_per_cell = int(updates_per_cell)
        
        
        if updates_per_cell <= 0:
            return
        
        
        upd = self.update
        emp = self.empty_fun()
        
        
        old = None
        new = self.lattice
        indexes = arrayIndexes(new.shape)
        for _ in range(updates_per_cell):
            
            
            old = new
            new = emp()
            
            
            for indx in indexes:
                upd(old, new, indx)
        
        
        self.lattice = new
        return
    
    
    def evolve_random(self, updates_per_cell = 1):
        
        
        n_cells = len(self)
        
        
        if not isinstance(updates_per_cell, int):
            updates_per_cell = float(updates_per_cell)
        if not numpy.isfinite(updates_per_cell):
            raise ValueError("invalid 'updates_per_cell' argument")
        
        
        n_updates = int(updates_per_cell * n_cells)
        
        
        if n_updates <= 0:
            return
        
        
        upd = self.update_random
        x = self.lattice
        indexes = arrayIndexes(x.shape)
        indexes = [indexes[i] for i in numpy.random.randint(len(indexes), size = n_updates)]
        for indx in indexes:
            
            
            # DO NOT GIVE THE USER x[indx]
            # THAT WOULD FAIL IF THE DATA IS NON-MUTABLE
            # GIVE THE LATTICE AND THE INDEX, LET THE USER
            # DEAL WITH EACH AS THEY NEED TO
            upd(x, indx)
        
        
        return
    
    
    pass

