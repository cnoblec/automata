import ca
import matplotlib.animation
import matplotlib.pyplot
import math
import numpy
import re





# each land use consists of:
# * an OP, an integer to identify the land use
# * a land use string, for printing
# * a colour, for plotting
# * a probability of being chosen, for initializing a random land use cell
# * a tuple of other acceptable strings, for input
INFO = numpy.array([
    [(WATEROP := 0), "water", "#56B4E9FF", 0.1, ("\U0001F4A7",)                       ],
    [(EARTHOP := 1), "earth", "#8B4513FF", 0.4, ("\U0001FAA8", "\u26F0", "\U0001F5FB")],
    [(FIREOP  := 2), "fire" , "#D55E00FF", 0.0, ("\U0001F525",)                       ],
    [(TREEOP  := 3), "tree" , "#009E73FF", 0.5, ("\U0001F333",)                       ],
], dtype = object)
OPS   = tuple(INFO[:, 0].astype(int))
LUS   = tuple(INFO[:, 1].astype(str))
COLS  = tuple([
    tuple([
        int(xx[i:(i + 2)], 16)
        for i in range(1, len(xx), 2)
    ])
    for xx in INFO[:, 2]
])
PROBS = tuple(INFO[:, 3].astype(float))
ALTS  = tuple(INFO[:, 4])
del INFO
if not numpy.array_equal(OPS, range(len(OPS))):
    raise ValueError(f"invalid OPS, should be 0:{len(OPS)}")


# dictionary to convert all interpretations of land_use to a valid OP
OPS_DICT = {
    lu:op
    for lu, op in zip(LUS, OPS)
} | {
    op:op
    for op in OPS
}
for tmp in [
    {alt:op for alt in alts}
    for alts, op in zip(ALTS, OPS)
]:
    OPS_DICT |= tmp


del tmp






# to specify a non-random land use cellular automata, specify an array of strings
# matching this Perl regular expression:
tmp = LUS + tuple(numpy.concatenate(ALTS))
lu_pattern = "\\A\\s*(" + "|".join(tmp) + ")\\s*(:\\s*(\\d+)\\s*)?\\Z"
#             ^^^                                                 ^^^ start and end of the string
#                ^^^^                       ^^^^  ^^^^      ^^^^      any number of whitespace characters
#                         ^^^^^^^^^^^^^                               one of the land use strings from above, or one of the alternatives
#                                                ^     ^^^^           a colon, and the age of the land use cell
#                                                                ^    the colon and age are optional
#                    ^^^^^^^^^^^^^^^^^^^^^^^                          group 0, the land use string
#                                               ^^^^^^^^^^^^^^^^^     group 1, unused
#                                                     ^^^^^^          group 2, the age of the land use cell
del tmp





##N_LUS = len(LUS)





N = max([
    len(lu)
    for lu in LUS
])
F_LUS   = [
    ("{:<" + str(N)     + "}").format(lu)
    for lu in LUS
]
del N


tmp = [
    repr(lu)
    for lu in LUS
]
N = max([
    len(lu)
    for lu in tmp
])
F_LUS_Q = [
    ("{:<" + str(N)     + "}").format(lu)
    for lu in tmp
]
del tmp
del N





class LandUseCell:
    
    
    def __init__(self, land_use, age = 0):
        
        
        """
        __init__                                                    Python Documentation

        Initialize an Object of Class "LandUseCell"



        Description:

        The constructor for class "LandUseCell" representing a cell in a land use
        cellular automata.



        Usage:

        LandUseCell(land_use, age = 0)



        Arguments:

        land_use

            integer or string; the land use type of the cell.

        age

            non-negative integer; the age of the cell.
        """
        
        
        self.__init2__(land_use, age)
        return
    
    
    def __init2__(self, land_use, age = 0, check = True):
        
        
        if check:
            land_use = OPS_DICT[land_use]
            
            
            if age is None:
                age = 0
            age = int(age)
            if age < 0:
                raise ValueError("invalid 'age'")
        
        
        self.land_use = land_use
        self.age = age
        return
    
    
    @staticmethod
    def from_string(x):
        
        
        """
        from_string                                                 Python Documentation

        Convert a String to LandUseCell



        Description:

        Convert a string specifying a land use type and age into a LandUseCell.



        Usage:

        from_string(x)



        Arguments:

        x

            string to convert to LandUseCell.



        Details:

        The string should follow this pattern:
        * one of the land use types ("water", "earth", "fire", "tree", ...)
        * optionally, a colon and an integer (the age of the cell)

        Whitespace may be added where desired.



        Value:

        An object of class "LandUseCell"
        """
        
        
        temp = re.search(lu_pattern, x)
        if temp is None:
            raise ValueError(f"invalid land use string '{x}'")
        temp = temp.groups()
        return LandUseCell(land_use = temp[0], age = temp[2])
    
    
    def __str__(self):
        
        
        """
        __str__                                                     Python Documentation

        Land Use Cell Conversion



        Description:

        Convert a land use cell to its string representation.



        Usage:

        str(self)
        repr(self)



        Details:

        The string representation will include the land use name and the age.



        Value:

        a string.
        """
        
        
        return f"{F_LUS[self.land_use]}:{self.age}"
    
    
    def __repr__(self):
        return f"LandUseCell({F_LUS_Q[self.land_use]}, age = {self.age})"
    
    
    __repr__.__doc__ = __str__.__doc__
    
    
    def __copy__(self):
        
        
        """
        __copy__                                                    Python Documentation

        Create a Copy of a Land Use Cell



        Description:

        Create a copy of a land use cell.



        Usage:

        copy.copy(self)
        self.copy()



        Value:

        An object of class "LandUseCell".
        """
        
        
        return _LandUseCell_no_check(self.land_use, self.age)
    
    
    copy = __copy__
    
    
    @staticmethod
    def random(p = PROBS):
        
        
        """
        random                                                      Python Documentation

        Create a Random Land Use Cell



        Description:

        Create a land use cell with a random land use type and age.



        Usage:

        LandUseCell.random()



        Details:

        Each land use type has a probability of appearing as indicated in 'PROBS'.
        The age will be a number from 0 to 24 inclusive.



        Value:

        An object of class "LandUseCell".
        """
        
        
        return _LandUseCell_no_check(
            numpy.random.choice(OPS, p = p),
            numpy.random.randint(25)
        )
    
    
    pass





def _LandUseCell_no_check(land_use, age = 0):
    value = LandUseCell.__new__(LandUseCell)
    value.__init2__(land_use, age, check = False)
    return value





def as_valid_p(x = None):
    if x is None:
        return PROBS
    if isinstance(x, dict):
        done = False
        special_keys = ["", -1]
        for key in special_keys:
            if key in x:
                value = x[key]
                if not isinstance(value, int | float):
                    raise ValueError(f"invalid value at key {repr(key)}, must be a number")
                if (not numpy.isfinite(value)) or value < 0:
                    raise ValueError(f"invalid value at key {repr(key)}, must be >= 0")
                p = numpy.full(len(OPS), value, float)
                done = True
                break
        if not done:
            p = numpy.zeros(len(OPS), float)
        for key, value in x.items():
            if key in special_keys:
                continue
            key = OPS_DICT[key]
            if not isinstance(value, int | float):
                raise ValueError(f"invalid value at key {repr(key)}, must be a number")
            if (not numpy.isfinite(value)) or value < 0:
                raise ValueError(f"invalid value at key {repr(key)}, must be >= 0")
            p[key] = value
    elif isinstance(x, tuple):
        if len(x) != len(OPS):
            raise ValueError(f"invalid 'x', expected a tuple of length {len(OPS)}, got {len(x)}")
        p = numpy.zeros(len(OPS), float)
        for key, value in enumerate(x):
            if not isinstance(value, int | float):
                raise ValueError(f"invalid value at element {repr(key)}, must be a number")
            if (not numpy.isfinite(value)) or value < 0:
                raise ValueError(f"invalid value at element {repr(key)}, must be >= 0")
            p[key] = value
    else:
        raise ValueError("invalid 'x', must be a dictionary or tuple")
    if p.sum() <= 0:
        raise ValueError("probabilities sum to 0")
    p /= p.sum()
    return tuple(p)





class LandUse(ca.CA):
    
    
    def __init__(self, shape = None, neighbour_order = None, lattice = None, p = None,
        age_parameters = None, random_parameters = None):
        
        
        """
        __init__                                                    Python Documentation
        
        Initialize an Object of Class "LandUse"
        
        
        
        Description:
        
        The constructor for class "LandUse" representing a lattice of land use types.
        
        
        
        Usage:
        
        LandUse(shape = None, neighbour_order = None, lattice = None, p = None,
            age_parameters = None, random_parameters = None)
        
        
        
        Arguments:
        
        shape
        
            integer or tuple of integers; the shape of the lattice.
        
        neighbour_order
        
            integer; how should the cells behave with their neighbouring cells?
        
        lattice
        
            an object of class numpy.ndarray; an alternative way to specify the state
            of the land use lattice. Should be all strings matching 'lu_pattern', see
            help(LandUseCell.from_string)

        p

            when 'lattice' is not specified, the probabilities for populating a random
            land use lattice. This is preferably a dictionary like:
            {
                "water" : 1,
                "earth" : 1,
                "fire"  : 0,
                "tree"  : 2,
                ...
            }
            If any land uses are not specified, they are assumed to be probability 0.
            This can be changed by adding {"" : n} or {-1 : n} to your dictionary:
            {
                "fire" : 0,
                "tree" : 3,
                ""     : 1,
            }
            is no fire, and 3 times as many trees.


        age_parameters

            a dictionary of integers; ages for which certain events will take place.
            Used in method 'update'.

        random_parameters

            a dictionary of functions accepting an age and returning True or False for
            an event taking place. Used in method 'update_random'.
        
        
        
        Details:
        
        You must provide either 'shape' or 'lattice', but not both.

        Currently, only 2D land use cellular automata are supported.
        """
        
        
        nargs = (shape is not None) + (lattice is not None)
        if nargs < 1:
            raise ValueError("provide either 'shape' or 'lattice'")
        if nargs > 1:
            raise ValueError("only one of 'shape' and 'lattice' can be used")
        which = "shape" if (shape is not None) else "lattice"
        
        
        if shape is not None:
            shape = numpy.empty(shape).shape
            p = as_valid_p(p)
        else:
            lattice = numpy.asarray(lattice, dtype = str)
            shape = lattice.shape
        if len(shape) != 2:
            raise NotImplementedError(f"invalid '{which}', {len(shape)} dimensional land use cellular automata are not yet implemented")
        super().__init__(
            shape = shape,
            cell_type = LandUseCell,
            neighbour_order = neighbour_order
        )
        
        
        age_params = {
            "water_turn_earth_to_tree" :  5,
             "tree_turn_earth_to_tree" :  3,
            "fire_to_earth"            :  5,
            "tree_to_fire"             : 25,
            "fire_turn_tree_to_fire"   :  5,
        }
        if isinstance(age_parameters, dict):
            for key in age_params.keys():
                if key in age_parameters:
                    age_params[key] = int(age_parameters[key])
                    if age_params[key] < 0:
                        raise ValueError("invalid 'age_parameters' value at key {repr(key)}, must be positive")
        self.age_params = age_params
        
        
        random_params = {
            "water_turn_earth_to_tree" : lambda age : numpy.random.random() < 0.1339745962155614,
             "tree_turn_earth_to_tree" : lambda age : numpy.random.random() < 0.1339745962155614,
            "fire_to_earth"            : lambda age : numpy.random.random() > math.exp(-age),
            "tree_to_fire"             : lambda age : numpy.random.random() > math.exp(-age/1000.0),
            "fire_turn_tree_to_fire"   : lambda age : numpy.random.random() < 0.25,
        }
        if isinstance(random_parameters, dict):
            for key in random_params.keys():
                if key in random_parameters:
                    random_params[key] = random_parameters[key]
                    if not callable(random_params[key]):
                        raise ValueError("invalid 'random_parameters' value at key {repr(key)}, must be callable")
        self.random_params = random_params
        
        
        if lattice is not None:
            for indx in numpy.ndindex(self.lattice.shape):
                self.lattice[indx] = LandUseCell.from_string(lattice[indx])
            self.p = None
        else:
            for indx in numpy.ndindex(self.lattice.shape):
                self.lattice[indx] = LandUseCell.random(p = p)
            self.p = p
        return
    
    
##    def __repr__(self):
##        
##        
##        """
##        __repr__                                                    Python Documentation
##
##        Cellular Automata Conversion
##
##
##
##        Description:
##
##        Convert a cellular automata to its string representation.
##
##
##
##        Usage:
##        
##        str(self)
##        repr(self)
##
##
##
##        Details:
##
##        The string representation will include the lattice, the lattice dimensions, and
##        the cell type.
##
##
##
##        Value:
##
##        a string.
##        """
##        
##        
##        return f"LandUse(lattice = {repr(self.lattice)}, neighbour_order = {repr(self.op)})"
    
    
##    def land_use_lattice(self):
##        return numpy.array([x.land_use for x in self.lattice.ravel()]).reshape(self.lattice.shape)
    
    
    def colour_lattice(self):
        
        
        """
        colour_lattice                                              Python Documentation

        Convert a Land Use Lattice to a Colour Lattice



        Description:

        Convert a land use cellular automata to its colour representation,
        for use with matplotlib.pyplot.imshow



        Usage:

        colour_lattice()
        color_lattice()



        Value:

        A numpy.ndarray with shape 'self.lattice.shape + (-1,)' and dtype int (from 0 to 255).
        """
        
        
        return numpy.array([
            COLS[x.land_use]
            for x in self.lattice.ravel()
        ]).reshape(self.lattice.shape + (-1,))
    
    
    color_lattice = colour_lattice
    
    
##    def update(self, x, indx):
##        xx = x[indx]
##        
##        
##        if xx.land_use == TREEOP:
##            
##            
##            for i in self.neighbours(indx):
##                
##                
##                # for a tree which neighbours an earth, grow a tree?
##                if x[i].land_use == EARTHOP and \
##                    xx.age >= 3:
##                    x[i].land_use = TREEOP
##                    x[i].age      = 0
##            
##            
##            # the tree lights on fire?
##            if xx.age >= 25:
##                xx.land_use = FIREOP
##                xx.age      = 0
##        
##        
##        elif xx.land_use == FIREOP:
##            
##            
##            for i in self.neighbours(indx):
##                
##                
##                # for a fire which neighbours a tree, ignite it?
##                if x[i].land_use == TREEOP and \
##                   xx.age >= 5:
##                    x[i].land_use = FIREOP
##                    x[i].age      = 0
##            
##            
##            # the fire extinguishes itself?
##            if xx.age >= 5:
##                xx.land_use = EARTHOP
##                xx.age      = 0
##            
##            
##        elif xx.land_use == WATEROP:
##            
##            
##            for i in self.neighbours(indx):
##                
##                
##                # for a water which neighbours an earth, grow a new tree?
##                if x[i].land_use == EARTHOP and \
##                   x[i].age >= 5:
##                    x[i].land_use = TREEOP
##                    x[i].age      = 0
##        
##        
##        xx.age += 1
##        return
    
    
    def update(self, old, new, indx):
        
        
        """
        update                                                      Python Documentation

        Update A Land Use Cell



        Description:

        Update the state of a land use cell (deterministically or randomly).



        Usage:

        update(old, new, indx)
        update_random(x, indx)



        Arguments:

        old, new, indx, x

            see help(CA.update)



        Details:

        For 'update', if the cell to update is:
        * earth type, it will turn into a tree if there is a nearby water or tree cell
              which is old enough is found
        * fire  type, it will extinguish itself if too old
        * tree  type, it will ignite itself if too old or a nearby fire which is old
              enough is found

        For 'update_random', the rules are similar, except that instead of based
        deterministically on age, they are based on decaying exponentials of age
        compared against random numbers.


   
        Value:

        None.
        """
        
        
        xx = new[indx] = old[indx].copy()
        
        
        if xx.land_use == EARTHOP:
            
            
            for i in self.neighbours(indx):
                
                
                # for an earth which neighbours a water or tree, turn into a tree?
                if (
                    old[i].land_use == WATEROP and \
                    xx.age >= self.age_params["water_turn_earth_to_tree"]
                ) or (
                    old[i].land_use == TREEOP  and \
                    old[i].age >= self.age_params["tree_turn_earth_to_tree"]
                ):
                    xx.land_use = TREEOP
                    xx.age      = 0
                    return
            
            
        elif xx.land_use == FIREOP:
            
            
            # the fire extinguishes itself?
            if xx.age >= self.age_params["fire_to_earth"]:
                xx.land_use = EARTHOP
                xx.age      = 0
                return
            
            
        elif xx.land_use == TREEOP:
            
            
            # the tree lights on fire?
            if xx.age >= self.age_params["tree_to_fire"]:
                xx.land_use = FIREOP
                xx.age      = 0
                return
            
            
            for i in self.neighbours(indx):
                
                
                # for a tree which neighbours a fire, ignite it?
                if (
                    old[i].land_use == FIREOP and \
                    old[i].age >= self.age_params["fire_turn_tree_to_fire"]
                ):
                    xx.land_use = FIREOP
                    xx.age      = 0
                    return
        
        
        xx.age += 1
        return
    
    
    def update_random(self, x, indx):
        xx = x[indx]
        
        
        if xx.land_use == EARTHOP:
            
            
            for i in self.neighbours(indx):
                
                
                # for an earth which neighbours a water or tree, turn into a tree?
                if (
                    x[i].land_use == WATEROP and \
                    self.random_params["water_turn_earth_to_tree"](xx.age)
                ) or (
                    x[i].land_use == TREEOP and \
                    self.random_params["tree_turn_earth_to_tree"](x[i].age)
                ):
                    xx.land_use = TREEOP
                    xx.age      = 0
                    return
            
            
        elif xx.land_use == FIREOP:
            
            
            # the fire extinguishes itself?
            if self.random_params["fire_to_earth"](xx.age):
                xx.land_use = EARTHOP
                xx.age      = 0
                return
            
            
        elif xx.land_use == TREEOP:
            
            
            # the tree lights on fire?
            if self.random_params["tree_to_fire"](xx.age):
                xx.land_use = FIREOP
                xx.age      = 0
                return
            
            
            for i in self.neighbours(indx):
                
                
                # for a tree which neighbours a fire, ignite it?
                if x[i].land_use == FIREOP and \
                   self.random_params["fire_turn_tree_to_fire"](x[i].age):
                    xx.land_use = FIREOP
                    xx.age      = 0
                    return
        
        
        xx.age += 1
        return
    
    
    update.__doc__ = update_random.__doc__
    
    
    def plot(self, ax = matplotlib.pyplot):
        return ax.imshow(self.colour_lattice())
    
    
    def animate(self, file = None, how = None, frames = 100, **save_kwargs):
        fig, ax = matplotlib.pyplot.subplots()
        if (how is None) or how == "deterministic":
            def fun(frame):
                if frame == 0:
                    ax.set_title("initial")
                else:
                    ax.set_title(f"step {frame}")
                    self.evolve()
                im.set_array(self.colour_lattice())
                return (im,)
        elif how == "random":
            def fun(frame):
                if frame == 0:
                    ax.set_title("initial")
                else:
                    ax.set_title(f"step {frame}")
                    self.evolve_random()
                im.set_array(self.colour_lattice())
                return (im,)
        else:
            raise ValueError("invalid 'how'")
        im = ax.imshow(numpy.full(self.lattice.shape + (3,), 255))
        value = matplotlib.animation.FuncAnimation(
            fig, fun, frames = numpy.arange(frames),
            blit = True, interval = 100
        )
        if file is not None:
            value.save(filename = file, **save_kwargs)
            matplotlib.pyplot.close(fig)
        return value
    
    
    pass

