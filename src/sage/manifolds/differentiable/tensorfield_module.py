r"""
Tensor field modules

The set of tensor fields along an open subset `U` of some differentiable
manifold `S` with values in a open subset `V` of a differentiable manifold `M`
(possibly `S=M` and `U=V`) is a module over the algebra `C^k(U)` of
differentiable scalar fields on `U`. It is a free module iff `V` is
parallelizable. Accordingly, two classes are devoted to tensor field modules:

- :class:`TensorFieldModule` for tensor fields with values in a generic (in
  practice, not parallelizable) open set `V`
- :class:`TensorFieldFreeModule` for tensor fields with values in a
  parallelizable open set `V`

AUTHORS:

- Eric Gourgoulhon, Michal Bejger (2014-2015): initial version

REFERENCES:

- S. Kobayashi & K. Nomizu : *Foundations of Differential Geometry*, vol. 1,
  Interscience Publishers (New York) (1963)
- J.M. Lee : *Introduction to Smooth Manifolds*, 2nd ed., Springer (New York)
  (2013)
- B O'Neill : *Semi-Riemannian Geometry*, Academic Press (San Diego) (1983)

"""

#******************************************************************************
#       Copyright (C) 2014 Eric Gourgoulhon <eric.gourgoulhon@obspm.fr>
#       Copyright (C) 2014 Michal Bejger <bejger@camk.edu.pl>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#******************************************************************************

from sage.structure.unique_representation import UniqueRepresentation
from sage.structure.parent import Parent
from sage.categories.modules import Modules
from sage.tensor.modules.tensor_free_module import TensorFreeModule
from sage.manifolds.differentiable.tensorfield import TensorField, \
                                                               TensorFieldParal
from sage.manifolds.differentiable.diff_form import DiffForm, DiffFormParal
from sage.manifolds.differentiable.automorphismfield import \
                                      AutomorphismField, AutomorphismFieldParal

class TensorFieldModule(UniqueRepresentation, Parent):
    r"""
    Module of tensor fields of a given type `(k,l)` along an open subset `U`
    of some differentiable manifold `S` with values in a open subset `V` of a
    differentiable manifold `M`,

    Given two non-negative integers `k` and `l` and a differentiable map

    .. MATH::

        \Phi:\ U\subset S \longrightarrow V\subset M

    the tensor field module `T^{(k,l)}(U,\Phi)` is the set of all tensor
    fields of the type

    .. MATH::

        t:\ U  \longrightarrow T^{(k,l)}M

    such that

    .. MATH::

        \forall p \in U,\ t(p) \in T^{(k,l)}(T_{\Phi(p)}M)

    i.e. `t(p)` is a tensor on the vector space `T_{\Phi(p)}M`.
    The set `T^{(k,l)}(U,\Phi)` is a module over `C^k(U)`, the ring
    (algebra) of differentiable scalar fields on `U` (see
    :class:`~sage.manifolds.differentiable.scalarfield_algebra.DiffScalarFieldAlgebra`).

    The standard case of tensor fields *on* a differentiable manifold
    corresponds to `S=M`, `U=V` and `\Phi = \mathrm{Id}_U`. Other common cases
    are `\Phi` being an immersion and `\Phi` being a curve in `V` (`U` is then
    an open interval of `\RR`).

    If `V` is parallelizable, the class :class:`TensorFieldFreeModule` should
    be used instead.

    This is a Sage *parent* class, the corresponding *element* class being
    :class:`~sage.manifolds.differentiable.tensorfield.TensorField`.

    INPUT:

    - ``vector_field_module`` -- module `\mathcal{X}(U,\Phi)` of vector
      fields along `U` associated with the map `\Phi: U \rightarrow V`.
    - ``tensor_type`` -- pair `(k,l)` with `k` being the contravariant rank and
      `l` the covariant rank

    EXAMPLE:

    Module of type-(2,0) tensor fields on the 2-sphere::

        sage: M = DiffManifold(2, 'M') # the 2-dimensional sphere S^2
        sage: U = M.open_subset('U') # complement of the North pole
        sage: c_xy.<x,y> = U.chart() # stereographic coordinates from the North pole
        sage: V = M.open_subset('V') # complement of the South pole
        sage: c_uv.<u,v> = V.chart() # stereographic coordinates from the South pole
        sage: M.declare_union(U,V)   # S^2 is the union of U and V
        sage: xy_to_uv = c_xy.transition_map(c_uv, (x/(x^2+y^2), y/(x^2+y^2)),
        ....:                                intersection_name='W', restrictions1= x^2+y^2!=0,
        ....:                                restrictions2= u^2+v^2!=0)
        sage: uv_to_xy = xy_to_uv.inverse()
        sage: W = U.intersection(V)
        sage: T20 = M.tensor_field_module((2,0)) ; T20
        Module T^(2,0)(M) of type-(2,0) tensors fields on the 2-dimensional
         differentiable manifold M

    `T^{(2,0)}(M)` is a module over the algebra `C^k(M)`::

        sage: T20.category()
        Category of modules over Algebra of differentiable scalar fields on the
         2-dimensional differentiable manifold M
        sage: T20.base_ring() is M.scalar_field_algebra()
        True

    `T^{(2,0)}(M)` is not a free module::

        sage: isinstance(T20, FiniteRankFreeModule)
        False

    because `M = S^2` is not parallelizable::

        sage: M.is_manifestly_parallelizable()
        False

    On the contrary, the module of type-(2,0) tensor fields on `U` is a free
    module, since `U` is parallelizable (being a coordinate domain)::

        sage: T20U = U.tensor_field_module((2,0))
        sage: isinstance(T20U, FiniteRankFreeModule)
        True
        sage: U.is_manifestly_parallelizable()
        True

    The zero element::

        sage: z = T20.zero() ; z
        Tensor field zero of type (2,0) on the 2-dimensional differentiable
         manifold M
        sage: z is T20(0)
        True
        sage: z[c_xy.frame(),:]
        [0 0]
        [0 0]
        sage: z[c_uv.frame(),:]
        [0 0]
        [0 0]

    The module `T^{(2,0)}(M)` coerces to any module of type-(2,0) tensor fields
    defined on some subdomain of `M`, for instance `T^{(2,0)}(U)`::

        sage: T20U.has_coerce_map_from(T20)
        True

    The reverse is not true::

        sage: T20.has_coerce_map_from(T20U)
        False

    The coercion::

        sage: T20U.coerce_map_from(T20)
        Conversion map:
          From: Module T^(2,0)(M) of type-(2,0) tensors fields on the 2-dimensional differentiable manifold M
          To:   Free module T^(2,0)(U) of type-(2,0) tensors fields on the Open subset U of the 2-dimensional differentiable manifold M

    The coercion map is actually the *restriction* of tensor fields defined
    on `M` to `U`::

        sage: t = M.tensor_field(2,0, name='t')
        sage: eU = c_xy.frame() ; eV = c_uv.frame()
        sage: t[eU,:] = [[2,0], [0,-3]]
        sage: t.add_comp_by_continuation(eV, W, chart=c_uv)
        sage: T20U(t)  # the conversion map in action
        Tensor field t of type (2,0) on the Open subset U of the 2-dimensional
         differentiable manifold M
        sage: T20U(t) is t.restrict(U)
        True

    There is also a coercion map from fields of tangent-space automorphisms to
    tensor fields of type (1,1)::

        sage: T11 = M.tensor_field_module((1,1)) ; T11
        Module T^(1,1)(M) of type-(1,1) tensors fields on the 2-dimensional
         differentiable manifold M
        sage: GL = M.automorphism_field_group() ; GL
        General linear group of the Module X(M) of vector fields on the
         2-dimensional differentiable manifold M
        sage: T11.has_coerce_map_from(GL)
        True

    Explicit call to the coercion map::

        sage: a = GL.one() ; a
        Field of tangent-space identity maps on the 2-dimensional
         differentiable manifold M
        sage: a.parent()
        General linear group of the Module X(M) of vector fields on the
         2-dimensional differentiable manifold M
        sage: ta = T11.coerce(a) ; ta
        Tensor field Id of type (1,1) on the 2-dimensional differentiable
         manifold M
        sage: ta.parent()
        Module T^(1,1)(M) of type-(1,1) tensors fields on the 2-dimensional
         differentiable manifold M
        sage: ta[eU,:]  # ta on U
        [1 0]
        [0 1]
        sage: ta[eV,:]  # ta on V
        [1 0]
        [0 1]

    """

    Element = TensorField

    def __init__(self, vector_field_module, tensor_type):
        r"""
        Construct a module of tensor fields taking values on a (a priori) not
        parallelizable differentiable manifold.

        TESTS::

            sage: M = DiffManifold(2, 'M') # the 2-dimensional sphere S^2
            sage: U = M.open_subset('U') # complement of the North pole
            sage: c_xy.<x,y> = U.chart() # stereographic coordinates from the North pole
            sage: V = M.open_subset('V') # complement of the South pole
            sage: c_uv.<u,v> = V.chart() # stereographic coordinates from the South pole
            sage: M.declare_union(U,V)   # S^2 is the union of U and V
            sage: xy_to_uv = c_xy.transition_map(c_uv, (x/(x^2+y^2), y/(x^2+y^2)),
            ....:                                intersection_name='W', restrictions1= x^2+y^2!=0,
            ....:                                restrictions2= u^2+v^2!=0)
            sage: XM = M.vector_field_module()
            sage: from sage.manifolds.differentiable.tensorfield_module import TensorFieldModule
            sage: T21 = TensorFieldModule(XM, (2,1)); T21
            Module T^(2,1)(M) of type-(2,1) tensors fields on the 2-dimensional
             differentiable manifold M
            sage: T21 is M.tensor_field_module((2,1))
            True
            sage: TestSuite(T21).run()

        """
        domain = vector_field_module._domain
        dest_map = vector_field_module._dest_map
        kcon = tensor_type[0]
        lcov = tensor_type[1]
        name = "T^(" + str(kcon) + "," + str(lcov) + ")(" + domain._name
        latex_name = r"\mathcal{T}^{(" + str(kcon) + "," + str(lcov) + \
                                               r")}\left(" + domain._latex_name
        if dest_map is domain._identity_map:
            name += ")"
            latex_name += r"\right)"
        else:
            name += "," + dest_map._name + ")"
            latex_name += "," + dest_map._latex_name + r"\right)"
        self._vmodule = vector_field_module
        self._tensor_type = tensor_type
        self._name = name
        self._latex_name = latex_name
        # the member self._ring is created for efficiency (to avoid calls to
        # self.base_ring()):
        self._ring = domain.scalar_field_algebra()
        Parent.__init__(self, base=self._ring, category=Modules(self._ring))
        self._domain = domain
        self._dest_map = dest_map
        self._ambient_domain = vector_field_module._ambient_domain
        # NB: self._zero_element is not constructed here, since no element
        # can be constructed here, to avoid some infinite recursion.

    #### Parent methods

    def _element_constructor_(self, comp=[], frame=None, name=None,
                              latex_name=None, sym=None, antisym=None):
        r"""
        Construct a tensor field.

        TESTS::

            sage: M = DiffManifold(2, 'M')
            sage: U = M.open_subset('U'); V = M.open_subset('V')
            sage: c_xy.<x,y> = U.chart(); c_uv.<u,v> = V.chart()
            sage: M.declare_union(U,V)
            sage: T20 = M.tensor_field_module((2,0))
            sage: t = T20._element_constructor_(comp=[[1+x, 2], [x*y, 3-y]], name='t'); t
            Tensor field t of type (2,0) on the 2-dimensional differentiable manifold M
            sage: t.display(c_xy.frame())
            t = (x + 1) d/dx*d/dx + 2 d/dx*d/dy + x*y d/dy*d/dx + (-y + 3) d/dy*d/dy
            sage: T20._element_constructor_(0) is T20.zero()
            True

        """
        if comp == 0:
            if not hasattr(self, '_zero_element'):
                self._zero_element = self._element_constructor_(name='zero',
                                                                latex_name='0')
                for frame in self._domain._frames:
                    if self._dest_map.restrict(frame._domain) == \
                                                               frame._dest_map:
                        self._zero_element.add_comp(frame)
                        # (since new components are initialized to zero)
            return self._zero_element
        if isinstance(comp, DiffForm):
            # coercion of a p-form to a type-(0,p) tensor:
            form = comp # for readability
            p = form.degree()
            if self._tensor_type != (0,p) or \
                                           self._vmodule != form.base_module():
                raise TypeError("cannot coerce the {}".format(form) +
                                " to an element of {}".format(self))
            if p == 1:
                asym = None
            else:
                asym = range(p)
            resu = self.element_class(self._vmodule, (0,p), name=form._name,
                                      latex_name=form._latex_name,
                                      antisym=asym)
            for dom, rst in form._restrictions.iteritems():
                resu._restrictions[dom] = dom.tensor_field_module((0,p))(rst)
            return resu
        if isinstance(comp, AutomorphismField):
            # coercion of an automorphism to a type-(1,1) tensor:
            autom = comp # for readability
            if self._tensor_type != (1,1) or \
                                          self._vmodule != autom.base_module():
                raise TypeError("cannot coerce the {}".format(autom) +
                                " to an element of {}".format(self))
            resu = self.element_class(self._vmodule, (1,1), name=autom._name,
                                      latex_name=autom._latex_name)
            for dom, rest in autom._restrictions.iteritems():
                resu._restrictions[dom] = dom.tensor_field_module((1,1))(rest)
            return resu
        if isinstance(comp, TensorField):
            # coercion by domain restriction
            if self._tensor_type == comp._tensor_type and \
               self._domain.is_subset(comp._domain) and \
               self._ambient_domain.is_subset(comp._ambient_domain):
                return comp.restrict(self._domain)
            else:
               raise TypeError("cannot coerce the {}".format(comp) +
                                " to an element of {}".format(self))

        # standard construction
        resu = self.element_class(self._vmodule, self._tensor_type, name=name,
                                  latex_name=latex_name, sym=sym,
                                  antisym=antisym)
        if comp != []:
            resu.set_comp(frame)[:] = comp
        return resu

    def _an_element_(self):
        r"""
        Construct some (unamed) tensor field.

        TEST::

            sage: M = DiffManifold(2, 'M')
            sage: U = M.open_subset('U'); V = M.open_subset('V')
            sage: c_xy.<x,y> = U.chart(); c_uv.<u,v> = V.chart()
            sage: M.declare_union(U,V)
            sage: T31 = M.tensor_field_module((3,1))
            sage: T31._an_element_()
            Tensor field of type (3,1) on the 2-dimensional differentiable manifold M

        """
        return self.element_class(self._vmodule, self._tensor_type)

    def _coerce_map_from_(self, other):
        r"""
        Determine whether coercion to ``self`` exists from other parent.

        TESTS::

            sage: M = DiffManifold(2, 'M')
            sage: U = M.open_subset('U')
            sage: T02 = M.tensor_field_module((0,2))
            sage: T02U = U.tensor_field_module((0,2))
            sage: T02U._coerce_map_from_(T02)
            True
            sage: T02._coerce_map_from_(T02U)
            False
            sage: T02._coerce_map_from_(M.diff_form_module(2))
            True
            sage: T11 = M.tensor_field_module((1,1))
            sage: T11._coerce_map_from_(M.automorphism_field_group())
            True

        """
        from sage.manifolds.differentiable.diff_form_module import \
                                                                 DiffFormModule
        from sage.manifolds.differentiable.automorphismfield_group import \
                                                         AutomorphismFieldGroup
        if isinstance(other, (TensorFieldModule, TensorFieldFreeModule)):
            # coercion by domain restriction
            return self._tensor_type == other._tensor_type and \
                   self._domain.is_subset(other._domain) and \
                   self._ambient_domain.is_subset(other._ambient_domain)
        if isinstance(other, DiffFormModule):
            # coercion of p-forms to type-(0,p) tensor fields
            return self._vmodule is other.base_module() and \
                                       self._tensor_type == (0, other.degree())
        if isinstance(other, AutomorphismFieldGroup):
            # coercion of automorphism fields to type-(1,1) tensor fields
            return self._vmodule is other.base_module() and \
                                                     self._tensor_type == (1,1)
        return False

    #### End of parent methods

    def _repr_(self):
        r"""
        Return a string representation of the object.

        TEST::

            sage: M = DiffManifold(2, 'M')
            sage: T13 = M.tensor_field_module((1,3))
            sage: T13._repr_()
            'Module T^(1,3)(M) of type-(1,3) tensors fields on the 2-dimensional differentiable manifold M'
            sage: repr(T13)  # indirect doctest
            'Module T^(1,3)(M) of type-(1,3) tensors fields on the 2-dimensional differentiable manifold M'
            sage: T13  # indirect doctest
            Module T^(1,3)(M) of type-(1,3) tensors fields on the 2-dimensional
             differentiable manifold M

        """
        description = "Module "
        if self._name is not None:
            description += self._name + " "
        description += "of type-({},{})".format(self._tensor_type[0],
                                                self._tensor_type[1])
        description += " tensors fields "
        if self._dest_map is self._domain._identity_map:
            description += "on the {}".format(self._domain)
        else:
            description += "along the {}".format(self._domain) + \
                           " mapped into the {}".format(self._ambient_domain)
        return description

    def _latex_(self):
        r"""
        Return a LaTeX representation of ``self``.

        TEST::

            sage: M = DiffManifold(2, 'M')
            sage: T13 = M.tensor_field_module((1,3))
            sage: T13._latex_()
            '\\mathcal{T}^{(1,3)}\\left(M\\right)'
            sage: latex(T13)  # indirect doctest
            \mathcal{T}^{(1,3)}\left(M\right)

        """
        if self._latex_name is None:
            return r'\mbox{' + str(self) + r'}'
        else:
           return self._latex_name

    def base_module(self):
        r"""
        Return the vector field module on which the tensor module is
        constructed.

        OUTPUT:

        - instance of class
          :class:`~sage.manifolds.differentiable.vectorfield_module.VectorFieldModule`
          representing the module on which the tensor module is defined.

        EXAMPLE::

            sage: M = DiffManifold(2, 'M')
            sage: T13 = M.tensor_field_module((1,3))
            sage: T13.base_module()
            Module X(M) of vector fields on the 2-dimensional differentiable manifold M
            sage: T13.base_module() is M.vector_field_module()
            True
            sage: T13.base_module().base_ring()
            Algebra of differentiable scalar fields on the 2-dimensional
             differentiable manifold M

        """
        return self._vmodule

    def tensor_type(self):
        r"""
        Return the tensor type of the tensor field module.

        OUTPUT:

        - pair `(k,l)` of non-negative integers such that the tensor fields
          belonging to this module are of type `(k,l)`

        EXAMPLES::

            sage: M = DiffManifold(2, 'M')
            sage: T13 = M.tensor_field_module((1,3))
            sage: T13.tensor_type()
            (1, 3)
            sage: T20 = M.tensor_field_module((2,0))
            sage: T20.tensor_type()
            (2, 0)

            """
        return self._tensor_type

#******************************************************************************

class TensorFieldFreeModule(TensorFreeModule):
    r"""
    Free module of tensor fields of a given type `(k,l)` along an open
    subset `U` of some differentiable manifold `S` with values in a
    parallelizable open subset `V` of a differentiable manifold `M`.

    Given two non-negative integers `k` and `l` and a differentiable map

    .. MATH::

        \Phi:\ U\subset S \longrightarrow V\subset M

    the tensor field module `T^{(k,l)}(U,\Phi)` is the set of all tensor
    fields of the type

    .. MATH::

        t:\ U  \longrightarrow T^{(k,l)}M

    such that

    .. MATH::

        \forall p \in U,\ t(p) \in T^{(k,l)}(T_{\Phi(p)}M)

    i.e. `t(p)` is a tensor on the vector space `T_{\Phi(p)}M`.

    The standard case of tensor fields *on* a differentiable manifold
    corresponds to `S=M`, `U=V` and `\Phi = \mathrm{Id}_U`. Other common cases
    are `\Phi` being an immersion and `\Phi` being a curve in `V` (`U` is then
    an open interval of `\RR`).

    Since `V` is parallelizable, the set `T^{(k,l)}(U,\Phi)` is a free
    module over `C^k(U)`, the ring (algebra) of differentiable scalar
    fields on `U` (see
    :class:`~sage.manifolds.differentiable.scalarfield_algebra.DiffScalarFieldAlgebra`).

    This is a Sage *parent* class, the corresponding *element* class being
    :class:`~sage.manifolds.differentiable.tensorfield.TensorFieldParal`.

    INPUT:

    - ``vector_field_module`` -- free module `\mathcal{X}(U,\Phi)` of vector
      fields along `U` associated with the map `\Phi: U \rightarrow V`.
    - ``tensor_type`` -- pair `(k,l)` with `k` being the contravariant rank and
      `l` the covariant rank

    EXAMPLE:

    Module of type-(2,0) tensor fields on `\RR^3`::

        sage: M = DiffManifold(3, 'R^3')
        sage: c_xyz.<x,y,z> = M.chart()  # Cartesian coordinates
        sage: T20 = M.tensor_field_module((2,0)) ; T20
        Free module T^(2,0)(R^3) of type-(2,0) tensors fields on the
         3-dimensional differentiable manifold R^3

    `T^{(2,0)}(\RR^3)` is a module over the algebra `C^k(\RR^3)`::

        sage: T20.category()
        Category of modules over Algebra of differentiable scalar fields on the
         3-dimensional differentiable manifold R^3
        sage: T20.base_ring() is M.scalar_field_algebra()
        True

    `T^{(2,0)}(\RR^3)` is a free module::

        sage: isinstance(T20, FiniteRankFreeModule)
        True

    because `M = R^3` is parallelizable::

        sage: M.is_manifestly_parallelizable()
        True

    The zero element::

        sage: z = T20.zero() ; z
        Tensor field zero of type (2,0) on the 3-dimensional differentiable
         manifold R^3
        sage: z[:]
        [0 0 0]
        [0 0 0]
        [0 0 0]

    A random element::

        sage: t = T20.an_element() ; t
        Tensor field of type (2,0) on the 3-dimensional differentiable
         manifold R^3
        sage: t[:]
        [2 0 0]
        [0 0 0]
        [0 0 0]

    The module `T^{(2,0)}(\RR^3)` coerces to any module of type-(2,0) tensor
    fields defined on some subdomain of `\RR^3`::

        sage: U = M.open_subset('U', coord_def={c_xyz: x>0})
        sage: T20U = U.tensor_field_module((2,0))
        sage: T20U.has_coerce_map_from(T20)
        True
        sage: T20.has_coerce_map_from(T20U)  # the reverse is not true
        False
        sage: T20U.coerce_map_from(T20)
        Conversion map:
          From: Free module T^(2,0)(R^3) of type-(2,0) tensors fields on the 3-dimensional differentiable manifold R^3
          To:   Free module T^(2,0)(U) of type-(2,0) tensors fields on the Open subset U of the 3-dimensional differentiable manifold R^3

    The coercion map is actually the *restriction* of tensor fields defined
    on `\RR^3` to `U`.

    There is also a coercion map from fields of tangent-space automorphisms to
    tensor fields of type (1,1)::

        sage: T11 = M.tensor_field_module((1,1)) ; T11
        Free module T^(1,1)(R^3) of type-(1,1) tensors fields on the
         3-dimensional differentiable manifold R^3
        sage: GL = M.automorphism_field_group() ; GL
        General linear group of the Free module X(R^3) of vector fields on the
         3-dimensional differentiable manifold R^3
        sage: T11.has_coerce_map_from(GL)
        True

    An explicit call to this coercion map is::

        sage: id = GL.one() ; id
        Field of tangent-space identity maps on the 3-dimensional
         differentiable manifold R^3
        sage: tid = T11(id) ; tid
        Tensor field Id of type (1,1) on the 3-dimensional differentiable
         manifold R^3
        sage: tid[:]
        [1 0 0]
        [0 1 0]
        [0 0 1]

    """

    Element = TensorFieldParal

    def __init__(self, vector_field_module, tensor_type):
        r"""
        Construct a module of tensor fields taking values on a
        parallelizable differentiable manifold.

        TESTS::

            sage: DiffManifold._clear_cache_() # for doctests only
            sage: M = DiffManifold(2, 'M')
            sage: X.<x,y> = M.chart()  # makes M parallelizable
            sage: XM = M.vector_field_module()
            sage: from sage.manifolds.differentiable.tensorfield_module import TensorFieldFreeModule
            sage: T12 = TensorFieldFreeModule(XM, (1,2)); T12
            Free module T^(1,2)(M) of type-(1,2) tensors fields on the
             2-dimensional differentiable manifold M
            sage: T12 is M.tensor_field_module((1,2))
            True
            sage: TestSuite(T12).run()

        """
        domain = vector_field_module._domain
        dest_map = vector_field_module._dest_map
        kcon = tensor_type[0]
        lcov = tensor_type[1]
        name = "T^(" + str(kcon) + "," + str(lcov) + ")(" + domain._name
        latex_name = r"\mathcal{T}^{(" + str(kcon) + "," + str(lcov) + \
                                               r")}\left(" + domain._latex_name
        if dest_map is domain._identity_map:
            name += ")"
            latex_name += r"\right)"
        else:
            name += "," + dest_map._name + ")"
            latex_name += "," + dest_map._latex_name + r"\right)"
        TensorFreeModule.__init__(self, vector_field_module, tensor_type,
                                  name=name, latex_name=latex_name)
        self._domain = domain
        self._dest_map = dest_map
        self._ambient_domain = vector_field_module._ambient_domain

    #### Parent methods

    def _element_constructor_(self, comp=[], frame=None, name=None,
                              latex_name=None, sym=None, antisym=None):
        r"""
        Construct a tensor field.

        TESTS::

            sage: M = DiffManifold(2, 'M')
            sage: X.<x,y> = M.chart()  # makes M parallelizable
            sage: T12 = M.tensor_field_module((1,2))
            sage: t = T12._element_constructor_(comp=[[[x,-y], [2,y]],
            ....:   [[1+x,y^2], [x^2,3]], [[x*y, 1-x], [y^2, x]]], name='t'); t
            Tensor field t of type (1,2) on the 2-dimensional differentiable
             manifold M
            sage: t.display()
            t = x d/dx*dx*dx - y d/dx*dx*dy + 2 d/dx*dy*dx + y d/dx*dy*dy
             + (x + 1) d/dy*dx*dx + y^2 d/dy*dx*dy + x^2 d/dy*dy*dx
             + 3 d/dy*dy*dy
            sage: T12._element_constructor_(0) is T12.zero()
            True

        """
        if comp == 0:
            return self._zero_element
        if isinstance(comp, DiffFormParal):
            # coercion of a p-form to a type-(0,p) tensor field:
            form = comp # for readability
            p = form.degree()
            if self._tensor_type != (0,p) or \
                                           self._fmodule != form.base_module():
                raise TypeError("cannot coerce the {}".format(form) +
                                " to an element of {}".format(self))
            if p == 1:
                asym = None
            else:
                asym = range(p)
            resu = self.element_class(self._fmodule, (0,p), name=form._name,
                                      latex_name=form._latex_name,
                                      antisym=asym)
            for frame, cp in form._components.iteritems():
                resu._components[frame] = cp.copy()
            return resu
        if isinstance(comp, AutomorphismFieldParal):
            # coercion of an automorphism to a type-(1,1) tensor:
            autom = comp # for readability
            if self._tensor_type != (1,1) or \
                                          self._fmodule != autom.base_module():
                raise TypeError("cannot coerce the {}".format(autom) +
                                " to an element of {}".format(self))
            resu = self.element_class(self._fmodule, (1,1), name=autom._name,
                                      latex_name=autom._latex_name)
            for basis, comp in autom._components.iteritems():
                resu._components[basis] = comp.copy()
            return resu
        if isinstance(comp, TensorField):
            # coercion by domain restriction
            if self._tensor_type == comp._tensor_type and \
               self._domain.is_subset(comp._domain) and \
               self._ambient_domain.is_subset(comp._ambient_domain):
                return comp.restrict(self._domain)
            else:
                raise TypeError("cannot coerce the {}".format(comp) +
                                " to an element of {}".format(self))
        # Standard construction
        resu = self.element_class(self._fmodule, self._tensor_type, name=name,
                                  latex_name=latex_name, sym=sym,
                                  antisym=antisym)
        if comp != []:
            resu.set_comp(frame)[:] = comp
        return resu

    # Rem: _an_element_ is declared in the superclass TensorFreeModule

    def _coerce_map_from_(self, other):
        r"""
        Determine whether coercion to ``self`` exists from other parent.

        TESTS::

            sage: M = DiffManifold(2, 'M')
            sage: X.<x,y> = M.chart()  # makes M parallelizable
            sage: U = M.open_subset('U', coord_def={X: x>0})
            sage: T02 = M.tensor_field_module((0,2))
            sage: T02U = U.tensor_field_module((0,2))
            sage: T02U._coerce_map_from_(T02)
            True
            sage: T02._coerce_map_from_(T02U)
            False
            sage: T02._coerce_map_from_(M.diff_form_module(2))
            True
            sage: T11 = M.tensor_field_module((1,1))
            sage: T11._coerce_map_from_(M.automorphism_field_group())
            True

        """
        from sage.manifolds.differentiable.diff_form_module import \
                                                             DiffFormFreeModule
        from sage.manifolds.differentiable.automorphismfield_group import \
                                                    AutomorphismFieldParalGroup
        if isinstance(other, (TensorFieldModule, TensorFieldFreeModule)):
            # coercion by domain restriction
            return self._tensor_type == other._tensor_type and \
                   self._domain.is_subset(other._domain) and \
                   self._ambient_domain.is_subset(other._ambient_domain)
        if isinstance(other, DiffFormFreeModule):
            # coercion of p-forms to type-(0,p) tensor fields
            return self._fmodule is other.base_module() and \
                                       self._tensor_type == (0, other.degree())
        if isinstance(other, AutomorphismFieldParalGroup):
            # coercion of automorphism fields to type-(1,1) tensor fields
            return self._fmodule is other.base_module() and \
                                                     self._tensor_type == (1,1)
        return False

    #### End of parent methods

    def _repr_(self):
        r"""
        Return a string representation of ``self``.

        TESTS::

            sage: M = DiffManifold(2, 'M')
            sage: X.<x,y> = M.chart()  # makes M parallelizable
            sage: T12 = M.tensor_field_module((1,2))
            sage: T12._repr_()
            'Free module T^(1,2)(M) of type-(1,2) tensors fields on the 2-dimensional differentiable manifold M'
            sage: repr(T12)  # indirect doctest
            'Free module T^(1,2)(M) of type-(1,2) tensors fields on the 2-dimensional differentiable manifold M'
            sage: T12  # indirect doctest
            Free module T^(1,2)(M) of type-(1,2) tensors fields on the
             2-dimensional differentiable manifold M

        """
        description = "Free module "
        if self._name is not None:
            description += self._name + " "
        description += "of type-({},{})".format(self._tensor_type[0],
                                                self._tensor_type[1])
        description += " tensors fields "
        if self._dest_map is self._domain._identity_map:
            description += "on the {}".format(self._domain)
        else:
            description += "along the {}".format(self._domain) + \
                           " mapped into the {}".format(self._ambient_domain)
        return description
