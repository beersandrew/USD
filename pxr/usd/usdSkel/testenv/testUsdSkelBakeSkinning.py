#!/pxrpythonsubst
#
# Copyright 2017 Pixar
#
# Licensed under the terms set forth in the LICENSE.txt file available at
# https://openusd.org/license.

from pxr import Gf, Sdf, Usd, UsdGeom, UsdSkel
import unittest


class TestUsdSkelBakeSkinning(unittest.TestCase):

    def test_DQSkinning(self):
        testFile = "dqs.usda"
        stage = Usd.Stage.Open(testFile)

        self.assertTrue(UsdSkel.BakeSkinning(stage.Traverse()))

        stage.GetRootLayer().Export("dqs.baked.usda")


    def test_DQSkinningWithInterval(self):
        testFile = "dqs.usda"
        stage = Usd.Stage.Open(testFile)

        self.assertTrue(UsdSkel.BakeSkinning(
            stage.Traverse(), Gf.Interval(1, 10)))

        stage.GetRootLayer().Export("dqs.bakedInterval.usda")


    def test_LinearBlendSkinning(self):
        testFile = "lbs.usda"
        stage = Usd.Stage.Open(testFile)

        self.assertTrue(UsdSkel.BakeSkinning(stage.Traverse()))

        stage.GetRootLayer().Export("lbs.baked.usda")


    def test_LinearBlendSkinningWithInterval(self):
        testFile = "lbs.usda"
        stage = Usd.Stage.Open(testFile)

        self.assertTrue(UsdSkel.BakeSkinning(
            stage.Traverse(), Gf.Interval(1, 10)))

        stage.GetRootLayer().Export("lbs.bakedInterval.usda")


    def test_BlendShapes(self):
        testFile = "blendshapes.usda"
        stage = Usd.Stage.Open(testFile)

        self.assertTrue(UsdSkel.BakeSkinning(stage.Traverse()))
        
        stage.GetRootLayer().Export("blendshapes.baked.usda")


    def test_BlendShapesWithNormals(self):
        testFile = "blendshapesWithNormals.usda"
        stage = Usd.Stage.Open(testFile)

        self.assertTrue(UsdSkel.BakeSkinning(stage.Traverse()))
        
        stage.GetRootLayer().Export("blendshapesWithNormals.baked.usda")

    def test_AncestorXformTimeSamples(self):
        # The time samples of an animated ancestor xform of a skinned mesh
        # must be baked, since the mesh's points compensate for its motion.
        layer = Sdf.Layer.CreateAnonymous(".usda")
        layer.ImportFromString('''#usda 1.0
def SkelRoot "Root" (prepend apiSchemas = ["SkelBindingAPI"])
{
    rel skel:skeleton = </Root/Skel>
    def Skeleton "Skel" (prepend apiSchemas = ["SkelBindingAPI"])
    {
        uniform token[] joints = ["A"]
        uniform matrix4d[] bindTransforms = [((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1))]
        uniform matrix4d[] restTransforms = [((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1))]
        rel skel:animationSource = </Root/Skel/Anim>
        def SkelAnimation "Anim"
        {
            uniform token[] joints = ["A"]
            float3[] translations.timeSamples = { 1: [(0,0,0)], 2: [(0,1,0)] }
            quatf[] rotations = [(1,0,0,0)]
            half3[] scales = [(1,1,1)]
        }
    }
    def Xform "MeshXf"
    {
        double3 xformOp:translate.timeSamples = { 1: (0,0,0), 10: (0,0,5) }
        uniform token[] xformOpOrder = ["xformOp:translate"]
        def Mesh "Mesh" (prepend apiSchemas = ["SkelBindingAPI"])
        {
            int[] faceVertexCounts = [3]
            int[] faceVertexIndices = [0, 1, 2]
            point3f[] points = [(0,0,0), (1,0,0), (0,1,0)]
            int[] primvars:skel:jointIndices = [0, 0, 0] (
                interpolation = "vertex"
                elementSize = 1
            )
            float[] primvars:skel:jointWeights = [1, 1, 1] (
                interpolation = "vertex"
                elementSize = 1
            )
        }
    }
}
''')
        stage = Usd.Stage.Open(layer)
        self.assertTrue(UsdSkel.BakeSkinning(stage.Traverse()))
        points = UsdGeom.Mesh(
            stage.GetPrimAtPath("/Root/MeshXf/Mesh")).GetPointsAttr()
        self.assertEqual(points.GetTimeSamples(), [1.0, 2.0, 10.0])


if __name__ == "__main__":
    unittest.main()
