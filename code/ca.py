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

    This helps to avoid issues when dealing with neighbours
    (no need to use a cycler or a remainder).
    
    
    
    Examples:
    
    arrayIndexes( (4, 5) )
    """
    
    
    # each line has a comment afterwards showing what is created
    # specifically for 'shape = (3, 4, 5)'
    
    
##    x = [numpy.arange(n) for n in shape]
##    # [array([0, 1, 2]), array([0, 1, 2, 3]), array([0, 1, 2, 3, 4])]
    
    
    # similar to the above code, but uses half positive indexes and half negative indexes
    x = [
        numpy.concatenate((
            numpy.arange(0,  (n + 1)//2),
            numpy.arange(-(n - 1)//2, 0)
        ))
        for n in shape
    ]
    # [array([ 0,  1, -1]), array([ 0,  1, -2, -1]), array([ 0,  1,  2, -2, -1])]
    
    
    # each element of the above arrays must be repeated 'each' times
    each = numpy.cumprod((1,) + shape[:0:-1])[::-1]
    # array([20,  5,  1])
    
    
    # after repeating the array with 'each',
    # the entire array must be repeated 'times' times
    times = numpy.prod(shape)//(shape * each)
    # array([ 1,  3, 12])
    
    
    return list(zip(*[
        numpy.concatenate([xx.repeat(eeach)] * ttimes)
        for xx, eeach, ttimes in zip(x, each, times)
    ]))





# each NEIGHBOUR consists of:
# * an OP, an integer to identify the neighbour order
# * a function which will return a list of the neighbouring indexes
#
# the OP values should be referred to by name only, the actual values could
# change at any time, but the names should not change
NEIGHBOURS = numpy.array([
    
    
    # 1D neighbours
    numpy.array([


        # first nearest neighbours in 1D
        [(NEIGHBOURS1D1OP := 0), (lambda indx : [
                                      (indx[0] - 1,),  # left  1
                                      (indx[0] + 1,),  # right 1
                                  ])
        ],

        
    ], dtype = object),
    
    
    # 2D neighbours
    numpy.array([


        # first nearest neighbours in 2D
        [(NEIGHBOURS2D1OP := 1), (lambda indx : [
                                      (indx[0] - 1, indx[1]    ),  # up    1,
                                      (indx[0]    , indx[1] - 1),  #        , left  1
                                      (indx[0]    , indx[1] + 1),  #        , right 1
                                      (indx[0] + 1, indx[1]    ),  # down  1,
                                  ])
        ],


        # second nearest neighbours in 2D
        [(NEIGHBOURS2D2OP := 2), (lambda indx : [
                                      (indx[0] - 1, indx[1] - 1),  # up   1, left  1
                                      (indx[0] - 1, indx[1]    ),  # up   1,
                                      (indx[0] - 1, indx[1] + 1),  # up   1, right 1
                                      (indx[0]    , indx[1] - 1),  #       , left  1
                                      (indx[0]    , indx[1] + 1),  #       , right 1
                                      (indx[0] + 1, indx[1] - 1),  # down 1, left  1
                                      (indx[0] + 1, indx[1]    ),  # down 1,
                                      (indx[0] + 1, indx[1] + 1),  # down 1, right 1
                                  ])
        ],

        
    ], dtype = object),
    
    
    # 3D neighbours
    numpy.array([


        # first nearest neighbours in 3D
        [(NEIGHBOURS3D1OP := 3), (lambda indx : [
                                      (indx[0] - 1, indx[1]    , indx[2]    ),  # x     , y     , z - 1
                                      (indx[0]    , indx[1] - 1, indx[2]    ),  # x     , y - 1 , z
                                      (indx[0]    , indx[1]    , indx[2] - 1),  # x - 1 , y     , z
                                      (indx[0]    , indx[1]    , indx[2] + 1),  # x + 1 , y     , z
                                      (indx[0]    , indx[1] + 1, indx[2]    ),  # x     , y + 1 , z
                                      (indx[0] + 1, indx[1]    , indx[2]    ),  # x     , y     , z + 1
                                  ])
        ],


        # second nearest neighbours in 3D
        [(NEIGHBOURS3D2OP := 4), (lambda indx : [
                                      (indx[0] - 1, indx[1] - 1, indx[2]    ),  # x     , y - 1 , z - 1
                                      (indx[0] - 1, indx[1]    , indx[2] - 1),  # x - 1 , y     , z - 1
                                      (indx[0] - 1, indx[1]    , indx[2]    ),  # x     , y     , z - 1
                                      (indx[0] - 1, indx[1]    , indx[2] + 1),  # x + 1 , y     , z - 1
                                      (indx[0] - 1, indx[1] + 1, indx[2]    ),  # x     , y + 1 , z - 1
                                      (indx[0]    , indx[1] - 1, indx[2] - 1),  # x - 1 , y - 1 , z
                                      (indx[0]    , indx[1] - 1, indx[2]    ),  # x     , y - 1 , z
                                      (indx[0]    , indx[1] - 1, indx[2] + 1),  # x + 1 , y - 1 , z
                                      (indx[0]    , indx[1]    , indx[2] - 1),  # x - 1 , y     , z
                                      (indx[0]    , indx[1]    , indx[2] + 1),  # x + 1 , y     , z
                                      (indx[0]    , indx[1] + 1, indx[2] - 1),  # x - 1 , y + 1 , z
                                      (indx[0]    , indx[1] + 1, indx[2]    ),  # x     , y + 1 , z
                                      (indx[0]    , indx[1] + 1, indx[2] + 1),  # x + 1 , y + 1 , z
                                      (indx[0] + 1, indx[1] - 1, indx[2]    ),  # x     , y - 1 , z + 1
                                      (indx[0] + 1, indx[1]    , indx[2] - 1),  # x - 1 , y     , z + 1
                                      (indx[0] + 1, indx[1]    , indx[2]    ),  # x     , y     , z + 1
                                      (indx[0] + 1, indx[1]    , indx[2] + 1),  # x + 1 , y     , z + 1
                                      (indx[0] + 1, indx[1] + 1, indx[2]    ),  # x     , y + 1 , z + 1
                                  ])
        ],


        # third nearest neighbours in 3D
        [(NEIGHBOURS3D3OP := 5), (lambda indx : [
                                      (indx[0] - 1, indx[1] - 1, indx[2] - 1),  # x - 1 , y - 1 , z - 1
                                      (indx[0] - 1, indx[1] - 1, indx[2]    ),  # x     , y - 1 , z - 1
                                      (indx[0] - 1, indx[1] - 1, indx[2] + 1),  # x + 1 , y - 1 , z - 1
                                      (indx[0] - 1, indx[1]    , indx[2] - 1),  # x - 1 , y     , z - 1
                                      (indx[0] - 1, indx[1]    , indx[2]    ),  # x     , y     , z - 1
                                      (indx[0] - 1, indx[1]    , indx[2] + 1),  # x + 1 , y     , z - 1
                                      (indx[0] - 1, indx[1] + 1, indx[2] - 1),  # x - 1 , y + 1 , z - 1
                                      (indx[0] - 1, indx[1] + 1, indx[2]    ),  # x     , y + 1 , z - 1
                                      (indx[0] - 1, indx[1] + 1, indx[2] + 1),  # x + 1 , y + 1 , z - 1
                                      (indx[0]    , indx[1] - 1, indx[2] - 1),  # x - 1 , y - 1 , z
                                      (indx[0]    , indx[1] - 1, indx[2]    ),  # x     , y - 1 , z
                                      (indx[0]    , indx[1] - 1, indx[2] + 1),  # x + 1 , y - 1 , z
                                      (indx[0]    , indx[1]    , indx[2] - 1),  # x - 1 , y     , z
                                      (indx[0]    , indx[1]    , indx[2] + 1),  # x + 1 , y     , z
                                      (indx[0]    , indx[1] + 1, indx[2] - 1),  # x - 1 , y + 1 , z
                                      (indx[0]    , indx[1] + 1, indx[2]    ),  # x     , y + 1 , z
                                      (indx[0]    , indx[1] + 1, indx[2] + 1),  # x + 1 , y + 1 , z
                                      (indx[0] + 1, indx[1] - 1, indx[2] - 1),  # x - 1 , y - 1 , z + 1
                                      (indx[0] + 1, indx[1] - 1, indx[2]    ),  # x     , y - 1 , z + 1
                                      (indx[0] + 1, indx[1] - 1, indx[2] + 1),  # x + 1 , y - 1 , z + 1
                                      (indx[0] + 1, indx[1]    , indx[2] - 1),  # x - 1 , y     , z + 1
                                      (indx[0] + 1, indx[1]    , indx[2]    ),  # x     , y     , z + 1
                                      (indx[0] + 1, indx[1]    , indx[2] + 1),  # x + 1 , y     , z + 1
                                      (indx[0] + 1, indx[1] + 1, indx[2] - 1),  # x - 1 , y + 1 , z + 1
                                      (indx[0] + 1, indx[1] + 1, indx[2]    ),  # x     , y + 1 , z + 1
                                      (indx[0] + 1, indx[1] + 1, indx[2] + 1),  # x + 1 , y + 1 , z + 1
                                  ])
        ],

        
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
        
            a type or a numpy.dtype (or something which can be converted to a numpy.dtype);
            the class of the objects in the lattice. If 'None', 'cell_type' will be
            inferred from 'lattice', and if 'lattice' is not provided, then 'cell_type'
            is 'object'.
        
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
        or 'None', where it is inferred from other arguments.
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
            if op not in OPS:
                raise ValueError("invalid 'neighbour_order'")
        
        
        if shape is not None:
            
            
            if cell_type is None:
                cell_type = object
            dtype = numpy.dtype(cell_type)
            
            
            # we want to call 'self.empty' to initialize an empty lattice,
            # but that relies on the lattice being already initialized
            # do the same idea without that assumption
            if   hasattr(self, "fill_value"):
                lattice = numpy.full (shape, self.fill_value, dtype)
            elif dtype in [bool, int, float, complex]:
                lattice = numpy.zeros(shape, dtype)
            else:
                lattice = numpy.empty(shape, dtype)
            
            
        else:
            
            
            if cell_type is None:
                lattice = numpy.asarray(lattice)
                cell_type = lattice.dtype
            else:
                lattice = numpy.asarray(lattice, dtype = cell_type)
        
        
        if lattice.ndim <= 0:
            raise ValueError(f"invalid '{which}', cannot use 0 dimensional array for a cellular automata")
        if lattice.ndim > len(OPS_LIST):
            raise ValueError(f"invalid '{which}', {lattice.ndim} dimensional cellular automata are not yet implemented")
        
        
        self.cell_type = cell_type
        self.lattice   = lattice
        
        
        if op is None:
            op = OPS_LIST[self.lattice.ndim - 1][0]
        else:
            if not (op in OPS_LIST[self.lattice.ndim - 1]):
                raise ValueError(f"invalid 'neighbour_order'")
        
        
        self.neighbour_order = self.op = op
        self.__neighbours = GETTERS[self.op]
        return
    
    
    def __len__(self):
        
        
        """
        __len__                                                     Python Documentation

        Number of Cells of a "CA"



        Description:

        Get the number of cells in a cellular automata.



        Usage:

        len(self)



        Value:

        An integer.
        """
        
        
        return self.lattice.size
    
    
    def items(self):
        
        
        """
        items                                                       Python Documentation

        Get Attributes of Cellular Automata



        Description:

        Get a tuple of attributes describing the cellular automata. Each attribute is a
        tuple, the first element being a key for the attribute, the second a value of
        the attribute. This is similar in behaviour to dict.items()



        Usage:

        items()



        Value:

        A tuple.
        """
        
        
        return (
                ("lattice"   , self.lattice      ) ,
                ("dimensions", self.lattice.shape) ,
                ("cell type" , self.cell_type    ) ,
        )
    
    
    def __str__(self):
        
        
        """
        __str__                                                     Python Documentation

        Cellular Automata Conversion



        Description:

        Convert a cellular automata to its string representation.



        Usage:
        
        str(self)
        repr(self)



        Details:

        The string representation will include the lattice, the lattice dimensions, and
        the cell type.



        Value:

        a string.
        """
        
        
        return f"An object of class \"{self.__class__.__name__}\"\n" + "".join([f"\n{key}:\n{value}\n" for key, value in self.items()])
    
    
##    def __repr__(self):
##        if isinstance(self.cell_type, type):
##            cell_type = self.cell_type.__name__
##        else:
##            cell_type = repr(self.cell_type)
##        return f"CA(cell_type = {cell_type}, lattice = {repr(self.lattice)}, neighbour_order = {repr(self.op)})"
##    
##    
##    __repr__.__doc__ = __str__.__doc__
    
    
    def __getitem__(self, indexes):
        
        
        """
        __getitem__                                                 Python Documentation

        Extract or Replace Parts of a CA



        Description:

        Extract or replace cells of a cellular automata. These methods simply call the
        same-name methods on the "lattice" attribute.



        Usage:

        self[indexes]
        self[indexes] = value



        Arguments:

        indexes, value

            arguments passed to further methods.



        Value:

        For 'self[indexes]', the cell or cells at those indexes.
        For 'self[indexes] = value', value.
        """
        
        
        return self.lattice.__getitem__(indexes)
    
    
    def __setitem__(self, indexes, value):
        return self.lattice.__setitem__(indexes, value)
    
    
    __setitem__.__doc__ = __getitem__.__doc__
    
    
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
        
            tuple of integers; an index of the lattice.
        
        Value:
        
        A list of tuples of integers.
        """
        
        
        return self.__neighbours(indx)
    
    
    def empty(self):
        
        
        """
        empty                                                       Python Documentation
        
        Create a New, Empty Lattice
        
        
        
        Description:
        
        Create a new, empty lattice (a temp lattice), useful for evolving the state of
        a cellular automata.
        
        
        
        Usage:
        
        empty()
        empty_fun()



        Details:

        If the cellular automata has an attribute "fill_value", it will be used with
        'numpy.full' to create an empty lattice.
        
        Otherwise, if the cellular automata's lattice is boolean, integer, float, or
        complex typed, 'numpy.zeros' will be used to create an empty lattice.

        Otherwise, 'numpy.empty' will be used to create an empty lattice.

        The purpose of 'empty_fun' is to be faster than 'empty' when called a repeated
        number of times by cutting out the 'hasattr' and 'dtype' condition testing.
        
        
        
        Note:
        
        These methods can be overloaded by a subclass as necessary.



        Value:

        For 'empty', a numpy.ndarray with the same shape and dtype as 'lattice'.

        For 'empty_fun', a function which will return a numpy.ndarray with the same
        shape and dtype as 'lattice'.
        """
        
        
        if   hasattr(self, "fill_value"):
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
    
    
    empty_fun.__doc__ = empty.__doc__
    
    
    @staticmethod
    def no_update_method():
        raise NotImplementedError("object has no 'update' or 'update_random' method, see help(CA.update)")
    
    
    def update(self, old, new, indx):
        
        
        """
        update                                                      Python Documentation

        Update A Cell



        Description:

        Update the state of a cell (deterministically or randomly), and possibly its'
        neighbouring cells.



        Usage:

        update(old, new, indx)
        update_random(x, indx)



        Arguments:

        old

            a numpy.ndarray; the old state of the lattice. DO NOT MODIFY.

        new

            a numpy.ndarray; the new state of the lattice, the temporary lattice.

        indx

            a tuple of integers; the index of the cell to be updated,
            and possibly its' neighbours.

        x

            a numpy.ndarray; the lattice to be updated.
            Specifically for update_random, a temporary lattice does not make sense,
            so none is provided.



        Details:

        The default methods will raise a NotImplementedError since there is no general
        method of updating a cell. Your CA subclass must overload these methods with
        their appropriate definitions.

        You will likely need the indexes of the neighbouring cells; they can easily be
        retrieved with 'self.neighbours(indx)'. The indexes of the neighbours are not
        included in the signature in the event that they are not needed.

        If 'update' or 'update_random' does not make sense for your CA subclass,
        define them as follows:

        def update(self, old, new, indx)
            raise NotImplementedError(f"'update' does not make sense for a cellular automata of class \\"{self.__class__.__name__}\\"")

        def update_random(self, x, indx)
            raise NotImplementedError(f"'update_random' does not make sense for a cellular automata of class \\"{self.__class__.__name__}\\"")



        Note:

        These methods should not be called directly. They are strictly intended for use
        in 'evolve' and 'evolve_random'.



        Value:

        None. Overloaded methods may return other objects, but their return values are
        not made use of by 'evolve' and 'evolve_random'.
        """
        
        
        self.no_update_method()
        return
    
    
    def update_random(self, x, indx):
        self.no_update_method()
        return
    
    
    update_random.__doc__= update.__doc__
    
    
    def evolve(self, updates_per_cell = 1):
        
        
        """
        evolve                                                      Python Documentation

        Evolve a Cellular Automata



        Description:

        Evolve the state of a cellular automata.



        Usage:

        evolve(updates_per_cell = 1)
        evolve_random(updates_per_cell = 1)



        Arguments:

        updates_per_cell

            number of times to update each cell while updating the whole lattice.
            In 'evolve_random', some cells may be updated more than this number,
            and some less; updates_per_cell is an average number of times to update
            each cell.



        Details:

        'evolve' will sequentially update each cell (lexically ordered), and will
        update the lattice 'updates_per_cell' number of times. 'updates_per_cell' will
        be converted to an integer.

        'evolve_random' will randomly update a cell, and will update
        'updates_per_cell * len(self)' cells in total. 'updates_per_cell' can be a float.



        Value:

        None.
        """
        
        
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
        
        
        if isinstance(updates_per_cell, int):
            
            
            # use 'int()' to get rid of any subclass
            n_updates = int(updates_per_cell) * n_cells
            
            
        else:
            
            
            # make sure 'updates_per_cell' is finite
            updates_per_cell = float(updates_per_cell)
            if not numpy.isfinite(updates_per_cell):
                raise ValueError("invalid 'updates_per_cell' argument")
            
            
            # this will be a float
            # if finite, convert to integer
            # if not, convert updates_per_cell to integer and redo multiplication
            n_updates = updates_per_cell * n_cells
            if numpy.isfinite(n_updates):
                n_updates = int(n_updates)
            else:
                n_updates = int(updates_per_cell) * n_cells
        
        
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
    
    
    evolve_random.__doc__ = evolve.__doc__
    
    
    pass

