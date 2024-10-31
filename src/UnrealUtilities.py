from unreal import (
    AssetToolsHelpers,
    AssetTools,
    EditorAssetLibrary,
    Material,
    MaterialFactoryNew,
    MaterialProperty,
    MaterialEditingLibrary,
    MaterialExpressionTextureSampleParameter2D as TextSample2D,
    AssetImportTask,
    FbxImportUI
)

import os

class UnrealUtility:
    def __init__(self):
        self.substanceRootDir = "/game/Substance"
        self.baseMaterialName = "M_SubstanceBase"
        self.substanceTempDir = "/game/Substance/Temp"
        self.baseMaterialPath = self.substanceRootDir + self.baseMaterialName
        self.baseColorName = "BaseColor"
        self.normalName = "Normal"
        self.occRoughnessMetallicName = "OcclusionRoughnessMetallic"

    def FindOrCreateBaseMaterial(self):
        if EditorAssetLibrary.does_asset_exist(self.baseMaterialPath):
            return EditorAssetLibrary.load_asset(self.baseMaterialPath)
        
        baseMat = AssetToolsHelpers.get_asset_tools().create_asset(self.baseMaterialName, self.substanceRootDir, Material, MaterialFactoryNew())
        baseColor = MaterialEditingLibrary.create_material_expression(baseMat, TextSample2D, -800, 0)
        baseColor.set_editor_property("parameter_name", self.baseColorName)
        MaterialEditingLibrary.connect_material_property(baseColor, "RGB", MaterialProperty.MP_BASE_COLOR)

        normal = MaterialEditingLibrary.create_material_expression(baseMat, TextSample2D, -800, 400)
        normal.set_editor_property("parameter_name", self.normalName)
        normal.set_editor_property("texture", EditorAssetLibrary.load_asset("/Engine/EngineMaterials/DefaultNormal"))
        MaterialEditingLibrary.connect_material_property(normal, "RGB", MaterialProperty.MP_NORMAL)

        occRoughnessMetallic = MaterialEditingLibrary.create_material_expression(baseMat, TextSample2D, -800, 800)
        occRoughnessMetallic.set_editor_property("parameter_name", self.occRoughnessMetallicName)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetallic, "R", MaterialProperty.MP_AMBIENT_OCCLUSION)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetallic, "G", MaterialProperty.MP_ROUGHNESS)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetallic, "B", MaterialProperty.MP_METALLIC)

        EditorAssetLibrary.save_asset(baseMat.get_path_name())
        return baseMat
    
    def LoadMeshFromPath(self, meshPath):
        meshName = os.path.split(meshPath)[-1].replace(".fbx","")
        importTask = AssetImportTask()
        importTask.replace_existing = True
        importTask.filename = meshPath
        importTask.destination_path = "/game/" + meshName
        importTask.save = True
        importTask.automated = True

        fbxImportOptions = FbxImportUI()
        fbxImportOptions.import_mesh = True
        fbxImportOptions.import_as_skeletal = False
        fbxImportOptions.import_materials = False
        fbxImportOptions.static_mesh_import_data.combine_meshes = True

        importTask.options = fbxImportOptions

        AssetToolsHelpers.get_asset_tools().import_asset_tasks([importTask])
        return importTask.get_objects()[0]
    
    
    def LoadFromDir(self, fileDir):
        for file in os.listdir(fileDir):
            if ".fbx" in file:
                self.LoadMeshFromPath(os.path.join(fileDir, file))
