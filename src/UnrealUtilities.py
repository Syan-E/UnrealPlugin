from unreal import (
    AssetToolsHelpers,  # Helper functions for asset tools
    AssetTools,  # Asset tools for managing assets
    EditorAssetLibrary,  # Library for editor asset operations
    Material,  # Material class
    MaterialFactoryNew,  # Factory for creating new materials
    MaterialProperty,  # Enum for material properties
    MaterialEditingLibrary,  # Library for editing materials
    MaterialExpressionTextureSampleParameter2D as TextSample2D,  # Texture sample parameter expression
    AssetImportTask,  # Task for importing assets
    FbxImportUI  # UI for importing FBX files
)

import os  # Importing the os module for operating system dependent functionality

class UnrealUtility:
    def __init__(self):
        self.substanceRootDir = "/game/Substance"  # Root directory for substance assets
        self.baseMaterialName = "M_SubstanceBase"  # Name of the base material
        self.substanceTempDir = "/game/Substance/Temp"  # Temporary directory for substance assets
        self.baseMaterialPath = self.substanceRootDir + self.baseMaterialName  # Full path to the base material
        self.baseColorName = "BaseColor"  # Name for the base color parameter
        self.normalName = "Normal"  # Name for the normal parameter
        self.occRoughnessMetallicName = "OcclusionRoughnessMetallic"  # Name for the occlusion, roughness, and metallic parameter

    def FindOrCreateBaseMaterial(self):
        if EditorAssetLibrary.does_asset_exist(self.baseMaterialPath):  # Check if the base material already exists
            return EditorAssetLibrary.load_asset(self.baseMaterialPath)  # Load and return the existing base material
        
        # Create a new base material if it doesn't exist
        baseMat = AssetToolsHelpers.get_asset_tools().create_asset(self.baseMaterialName, self.substanceRootDir, Material, MaterialFactoryNew())
        
        # Create and configure the base color parameter
        baseColor = MaterialEditingLibrary.create_material_expression(baseMat, TextSample2D, -800, 0)
        baseColor.set_editor_property("parameter_name", self.baseColorName)
        MaterialEditingLibrary.connect_material_property(baseColor, "RGB", MaterialProperty.MP_BASE_COLOR)

        # Create and configure the normal parameter
        normal = MaterialEditingLibrary.create_material_expression(baseMat, TextSample2D, -800, 400)
        normal.set_editor_property("parameter_name", self.normalName)
        normal.set_editor_property("texture", EditorAssetLibrary.load_asset("/Engine/EngineMaterials/DefaultNormal"))
        MaterialEditingLibrary.connect_material_property(normal, "RGB", MaterialProperty.MP_NORMAL)

        # Create and configure the occlusion, roughness, and metallic parameter
        occRoughnessMetallic = MaterialEditingLibrary.create_material_expression(baseMat, TextSample2D, -800, 800)
        occRoughnessMetallic.set_editor_property("parameter_name", self.occRoughnessMetallicName)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetallic, "R", MaterialProperty.MP_AMBIENT_OCCLUSION)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetallic, "G", MaterialProperty.MP_ROUGHNESS)
        MaterialEditingLibrary.connect_material_property(occRoughnessMetallic, "B", MaterialProperty.MP_METALLIC)

        EditorAssetLibrary.save_asset(baseMat.get_path_name())  # Save the new base material
        return baseMat  # Return the created base material
    
    def LoadMeshFromPath(self, meshPath):
        meshName = os.path.split(meshPath)[-1].replace(".fbx", "")  # Extract the mesh name from the file path
        importTask = AssetImportTask()  # Create a new asset import task
        importTask.replace_existing = True  # Set to replace existing assets
        importTask.filename = meshPath  # Set the file path for the mesh
        importTask.destination_path = "/game/" + meshName  # Set the destination path for the imported mesh
        importTask.save = True  # Set to save the imported asset
        importTask.automated = True  # Set to automate the import process

        fbxImportOptions = FbxImportUI()  # Create a new FBX import UI
        fbxImportOptions.import_mesh = True  # Set to import the mesh
        fbxImportOptions.import_as_skeletal = False  # Set to import as a static mesh
        fbxImportOptions.import_materials = False  # Set to not import materials
        fbxImportOptions.static_mesh_import_data.combine_meshes = True  # Set to combine meshes

        importTask.options = fbxImportOptions  # Assign the import options to the task

        AssetToolsHelpers.get_asset_tools().import_asset_tasks([importTask])  # Execute the import task
        return importTask.get_objects()[0]  # Return the imported mesh object
    
    def LoadFromDir(self, fileDir):
        for file in os.listdir(fileDir):  # Iterate through files in the directory
            if ".fbx" in file:  # Check if the file is an FBX file
                self.LoadMeshFromPath(os.path.join(fileDir, file))  # Load the mesh from the file path