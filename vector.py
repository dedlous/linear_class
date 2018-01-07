from math import sqrt, acos, pi
from decimal import Decimal,getcontext

getcontext().prec=5
class Vector(object):
    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'cannot normalize zero vector'
    NO_UNIQUE_PARALLEL_COMPONENT_MSG='CANNOT_NORMALIZE_ZERO_VECTOR_MSG'
    ONLY_DEFINED_IN_TWOTHREE_DIMS_MSG='ONLY_DEFINED_IN_TWOTHREE_DIMS_MSG'
    def __init__(self, coordinates):


        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(self.coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def __getitem__(self, item):
        return self.coordinates[item]

    def plus(self,v):
        new_coordinates=[x+y for x,y in zip(self.coordinates ,v.coordinates)]
        return Vector(new_coordinates)

    def minus(self,v):
        new_coordinates=[x-y for x,y in zip(self.coordinates ,v.coordinates)]
        return Vector(new_coordinates)

    def times_scalar(self,n):
        new_coordinates=[ Decimal(n)*x for x in self.coordinates ]
        return Vector(new_coordinates)

    def magnitude(self):
        coordinates_squared=[ x*x for x in self.coordinates]
        return Decimal(sqrt(sum(coordinates_squared)))

    def normalized(self):
        try:
            magnitude=self.magnitude()
            return self.times_scalar(Decimal(1.0)/magnitude)

        except ZeroDivisionError:
            raise Exception('zero devider')

    def dot(self,v):
        return sum(x*y for x,y in zip(self.coordinates,v.coordinates))

    def angle_with(self,v,in_degrees=True):
        try:
            u1=self.normalized()
            u2=v.normalized()
            angle_in_radians=acos(u1.dot(u2))
            if in_degrees:
                degrees_per_radians=180.0/pi
                return angle_in_radians*degrees_per_radians
            else:
                return angle_in_radians

        except Exception as e :
            if str(e)==self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('cannot normalize zero vector')
            else :
                raise e

    def is_orthogonal_to(self,v,tolerance=1e-10):
        return abs(self.dot(v))<tolerance

    def is_parallel_to(self,v):
        return (self.is_zero() or v.is_zero() or self.angle_with(v)==0 or self.angle_with(v)==180)

    def is_zero(self,tolerance=1e-10):
        return self.magnitude()<tolerance

    def component_parallel_to(self,basis):
        try:
            u=basis.normalized()
            weight=self.dot(u)
            return u.times_scalar(weight)
        except Exception as e:
            if str(e)==self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise  Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)
            else :
                raise e

    def component_orthogonal_to(self,basis):
        try:
            projection=self.component_parallel_to(basis)
            return self.minus(projection)
        except  Exception as e:
            if str(e)==self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)

    def cross(self,v):
        try:
            x_1,y_1,z_1=self.coordinates
            x_2,y_2,z_2=v.coordinates
            new_coordiantes=[ y_1*z_2-y_2*z_1,
                              -(x_1*z_2-x_2*z_1),
                              x_1*y_2-x_2*y_1  ]
            return Vector(new_coordiantes)
        except Exception as e:
            msg=str(e)
            if msg=='need more than 2 values to unpack':
                self_embedded_in_R3=Vector(self.coordinates+('0',))
                v_embedded_in_R3=Vector(v.coordinates+('0',))
                return self_embedded_in_R3.cross(v_embedded_in_R3)
            elif (msg=='too many valus to unpack' or
                  msg =='need more than 1 valus to unpack'):
                raise Exception(self.ONLY_DEFINED_IN_TWOTHREE_DIMS_MSG)
            else:
                raise e
    def area_of_parallelogram_with(self,v):
        cross_product=self.cross(v)
        return cross_product.magnitude()

    def area_of_traiangle_with(self,v):
        return self.area_of_parallelogram_with(v)/Decimal('2.0')

print Vector([3,3]).angle_with(Vector([-3,-3]))
'''
vector1=Vector([3,4,5,6])
vector2=Vector([2,5,4,7])
print vector1.minus(vector2)
print vector1.times_scalar(10)


print Vector([3,4]).magnitude()
print Vector([3,4]).normalized()
print Vector([3,4]).dot(Vector([1,1]))
print Vector([3,3]).angle_with(Vector([-3,-3]))
print Vector([3,3]).is_parallel_to(Vector([-3,-3]))
print 'parallel vector / orthogonal vector'
print Vector([3.039,1.879]).component_parallel_to(Vector([0.825,2.036]))
print Vector([-9.88,-3.264,-8.159]).component_orthogonal_to(Vector([-2.155,-9.353,-9.473]))
print 'cross product'
print Vector([8.462,7.893,-8.187]).cross(Vector([6.984,-5.975,4.778]))

'''



















