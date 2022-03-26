import numpy





NEIGHBOURS = numpy.array([
    
    
    # 1D neighbours
    numpy.array([
        [(NEIGHBOURS1D2OP := 0), (lambda index : [
                                      index - 1,  # left  1
                                      index + 1   # right 1
                                  ])
        ]
    ], dtype = object),
    
    
    # 2D neighbours
    numpy.array([
        [(NEIGHBOURS2D4OP := 1), (lambda index , nrow : [
                                      index + 1       ,  # right 1
                                      index     - nrow,  # up    1
                                      index - 1       ,  # left  1
                                      index     + nrow   # down  1
                                  ])
        ],
        [(NEIGHBOURS2D8OP := 2), (lambda index , nrow : [
                                      index + 1       ,  # right 1
                                      index + 1 - nrow,  # right 1 up   1
                                      index     - nrow,  #         up   1
                                      index - 1 - nrow,  # left  1 up   1
                                      index - 1       ,  # left  1
                                      index - 1 + nrow,  # left  1 down 1
                                      index     + nrow,  #         down 1
                                      index + 1 + nrow   # right 1 down 1
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
            return numpy.full (len(self), self.fill_value, self.lattice.dtype)
        elif self.lattice.dtype in [bool, int, float, complex]:
            return numpy.zeros(len(self), self.lattice.dtype)
        else:
            return numpy.empty(len(self), self.lattice.dtype)
    
    
    def empty_fun(self):
        shape = len(self)
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
    
    
    def neighbours(self, index):
        
        
        """
        neighbours                                                  Python Documentation
        
        Get Indexes of Lattice Neighbours
        
        
        
        Description:
        
        Get a list of the indexes of the neighbouring cells.
        
        
        
        Usage:
        
        neighbours(index)
        
        
        
        Arguments:
        
        index
        
            integer; an index of the lattice. This function is intended to receive an
            index of a flat lattice and return the neighbouring cells flat indexes.
            This is mostly for convenience, it's annoying (but not impossible) to index an
            arbitrarily sized lattice, but very easy to index a 1D lattice.
        
        Value:
        
        A list of integers.
        """
        
        
        if self.lattice.ndim == 1:
            return self.__neighbours(index)
        elif self.lattice.ndim == 2:
            return self.__neighbours(index, self.lattice.shape[0])
        raise NotImplementedError("'neighbours' unimplemented for {self.lattice.ndim} dimensions")
    
    
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
        
        
        # we use ravel (instead of flatten) because it doesn't copy data
        flat_lattice = self.lattice.ravel()
        
        
        # better than the old, starts at index 0, but still avoids the extreme numbers
        flat_indx = numpy.concatenate((
            numpy.arange(0,  (n_cells + 1)//2),
            numpy.arange(-(n_cells - 1)//2, 0)
        ))
##        flat_indx = numpy.arange(
##            -n_cells//2,
##            -n_cells//2 + n_cells
##        )
        
        
        upd = self.update
        emp = self.empty_fun()
        
        
        old = None
        new = flat_lattice
        for _ in range(updates_per_cell):
            
            
            old = new
            new = emp()
            
            
            for indx in flat_indx:
                upd(old, new, indx)


        self.lattice = new.reshape(self.lattice.shape)
        return
    
    
    def evolve_random(self, updates_per_cell = 1):
        
        
        n_cells = len(self)
        
        
        updates_per_cell = float(updates_per_cell)
        if not numpy.isfinite(updates_per_cell):
            raise ValueError("invalid 'updates_per_cell' argument")
        
        
        n_updates = int(updates_per_cell * n_cells)
        
        
        if n_updates <= 0:
            return
        
        
        # we use ravel (instead of flatten) because it doesn't copy data
        flat_lattice = self.lattice.ravel()
        flat_indx = numpy.random.randint(
            low  = -(n_cells - 1)//2, 
            high =  (n_cells + 1)//2,
            size = n_updates
        )
        upd = self.update_random
        for indx in flat_indx:
            
            
            # DO NOT GIVE THE USER flat_lattice[indx]
            # THAT WOULD FAIL IF THE DATA IS NON-MUTABLE
            # GIVE THE LATTICE AND THE INDEX, LET THE USER
            # DEAL WITH EACH AS THEY NEED TO
            upd(flat_lattice, indx)
        
        
        return
    
    
    pass
