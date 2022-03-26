import ca
import matplotlib.pyplot
import math
import numpy
import re





INFO = numpy.array([
    [(WATEROP := 0), "water", "#56B4E9FF", 0.1],
    [(EARTHOP := 1), "earth", "#8B4513FF", 0.4],
    [(FIREOP  := 2), "fire" , "#D55E00FF", 0.0],
    [(TREEOP  := 3), "tree" , "#009E73FF", 0.5]
], dtype = object)
OPS       = INFO[:, 0].astype(int)
LAND_USES = INFO[:, 1].astype(str)
COLS      = [tuple([int(xx[i:(i + 2)], 16) for i in range(1, len(xx), 2)]) for xx in INFO[:, 2]]
PROBS     = INFO[:, 3].astype(float)
del INFO
if not numpy.array_equal(OPS, range(len(OPS))):
    raise ValueError(f"invalid OPS, should be 0:{len(OPS)}")





land_use_pattern = "\\A\\s*(" + "|".join(LAND_USES) + ")\\s*(:\\s*(\\d+)\\s*)?\\Z"




N_LAND_USES = len(LAND_USES)





N = max([len(x) for x in LAND_USES])
F_LAND_USES        = [("{:<" + str(N)     + "}").format(x) for x in LAND_USES]
F_LAND_USES_QUOTED = [("{:<" + str(N + 2) + "}").format("\"" + x + "\"") for x in LAND_USES]
del N





class LandUseCell:
    
    
    def __init2__(self, land_use, age = 0, check = True):
        
        
        if check:
            if isinstance(land_use, bool | int | float):
                land_use = int(land_use)
                if not (land_use in range(N_LAND_USES)):
                    raise ValueError("invalid 'land_use'")
            
            
            elif isinstance(land_use, str):
                for i in range(N_LAND_USES):
                    if land_use == LAND_USES[i]:
                        land_use = i
                        break
                
                
                if isinstance(land_use, str):
                    raise ValueError("invalid 'land_use'")
            
            
            else:
                raise ValueError("invalid 'land_use'")
            
            
            if age is None:
                age = 0
            age = int(age)
            if age < 0:
                raise ValueError("invalid 'age'")
        
        
        self.land_use = land_use
        self.age = age
        return
    
    
    def __init__(self, land_use, age = 0):
        self.__init2__(land_use, age)
        return
    
    
    def __repr__(self):
        return f"LandUseCell({F_LAND_USES_QUOTED[self.land_use]}, age = {self.age})"
    
    
    def __str__(self):
        return f"{F_LAND_USES[self.land_use]}:{self.age}"
    
    
    def __copy__(self):
        return _LandUseCell_no_check(self.land_use, self.age)
    
    
    def copy(self):
        return _LandUseCell_no_check(self.land_use, self.age)
    
    
    def random_cell():
        return _LandUseCell_no_check(
            numpy.random.choice(OPS, p = PROBS),
            numpy.random.randint(25)
        )
    
    
    pass





def _LandUseCell_no_check(land_use, age = 0):
    value = LandUseCell.__new__(LandUseCell)
    value.__init2__(land_use, age, check = False)
    return value





class LandUse(ca.CA):
    
    
    def __init__(self, shape = None, neighbour_order = None, lattice = None):
        if not (lattice is None):
            if not (shape is None):
                raise ValueError("only one of 'shape' and 'lattice' can be used")
            lattice = numpy.asarray(lattice, dtype = str)
            shape = lattice.shape
        else:
            shape = numpy.empty(shape).shape
        if len(shape) != 2:
            raise NotImplementedError(f"invalid 'shape', {len(shape)} dimensional land use automata are not yet implemented")
        super().__init__(
            shape = shape,
            cell_type = LandUseCell,
            neighbour_order = neighbour_order
        )
        if not (lattice is None):
            shape = self.lattice.shape
            self.lattice.shape = (self.lattice.size,)
            indx = -1
            for x in lattice.ravel():
                temp = re.search(land_use_pattern, x)
                if temp is None:
                    raise ValueError(f"invalid land use string '{xx}'")
                temp = temp.groups()
                indx += 1
                self.lattice[indx] = LandUseCell(land_use = temp[0], age = temp[2])
            self.lattice.shape = shape
##            for indx in numpy.ndindex(self.lattice.shape):
##                temp = re.search(land_use_pattern, lattice[indx])
##                if temp is None:
##                    raise ValueError(f"invalid land use string '{xx}'")
##                temp = temp.groups()
##                self.lattice[indx] = LandUseCell(land_use = temp[0], age = temp[2])
        else:
            for indx in numpy.ndindex(self.lattice.shape):
                self.lattice[indx] = LandUseCell.random_cell()
        return
    
    
    def land_use_lattice(self):
        return numpy.array([x.land_use for x in self.lattice.ravel()]).reshape(self.lattice.shape)
    
    
    def colour_lattice(self):
        return numpy.array([COLS[x.land_use] for x in self.lattice.ravel()]).reshape(self.lattice.shape + (4,))
    
    
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
        xx = new[indx] = old[indx].copy()
        
        
        if xx.land_use == EARTHOP:
            
            
            for i in self.neighbours(indx):
                
                
                # for an earth which neighbours a water or tree, turn into a tree?
                if (
                    old[i].land_use == WATEROP and \
                    old[i].age >= 5            and \
                        xx.age >= 5
                ) or (
                    old[i].land_use == TREEOP  and \
                    old[i].age >= 3
                ):
                    xx.land_use = TREEOP
                    xx.age      = 0
                    return
            
            
        elif xx.land_use == FIREOP:
            
            
            # the fire extinguishes itself?
            if xx.age >= 5:
                xx.land_use = EARTHOP
                xx.age      = 0
                return
            
            
        elif xx.land_use == TREEOP:
            
            
            # the tree lights on fire?
            if xx.age >= 25:
                xx.land_use = FIREOP
                xx.age      = 0
                return
            
            
            for i in self.neighbours(indx):
                
                
                # for a tree which neighbours a fire, ignite it?
                if (
                    old[i].land_use == FIREOP and \
                    old[i].age >= 5
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
                
                
                # for an earth which neighbours a tree, turn into a tree?
                if x[i].land_use == TREEOP and \
                   numpy.random.random() < 0.25:
                    xx.land_use = TREEOP
                    xx.age      = 0
                    return
            
            
        elif xx.land_use == FIREOP:
            
            
            # the fire extinguishes itself?
            if numpy.random.random() > math.exp(-xx.age):
                xx.land_use = EARTHOP
                xx.age      = 0
                return
            
            
        elif xx.land_use == TREEOP:
            
            
            # the tree lights on fire?
            if numpy.random.random() > math.exp(-xx.age/1000.0):
                xx.land_use = FIREOP
                xx.age      = 0
                return
            
            
            for i in self.neighbours(indx):
                
                
                # for a tree which neighbours a fire, ignite it?
                if x[i].land_use == FIREOP and \
                   numpy.random.random() < 0.25:
                    xx.land_use = FIREOP
                    xx.age      = 0
                    return
        
        
        xx.age += 1
        return
    
    
    def plot(self):
        return matplotlib.pyplot.imshow(self.colour_lattice())
    
    
    def animate(self, which = None):
        if (which is None) or which == "deterministic":
            def fun(frame):
                self.evolve()
                im.set_array(self.colour_lattice())
                return im,
        elif which == "random":
            def fun(frame):
                self.evolve_random()
                im.set_array(self.colour_lattice())
                return im,
        
        fig = matplotlib.pyplot.figure()
        im = self.plot()
        return matplotlib.animation.FuncAnimation(
            fig, fun, frames = numpy.arange(200),
            blit = True, interval = 100
        )
    
    
    pass

