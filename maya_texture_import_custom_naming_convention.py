#   EMILIA STEVENS

#IN MAYA:

# import texture_import_dae_naming_convention as swt
# import imp
# imp.reload(swt)

from maya import cmds
import os

class ShaderWithSelectedTextures:
    def __init__(self):
        '''initialization of the UI'''

        "---------------------------------------------- GLOBAL VARIABLES ----------------------------------------"

        #INITIALIZE NAMING CONVENTION and WORKING COLOR SPACE
        self.naming_convention_string = "projectcode_assetlib_asset_task_version_texturetype"
        self.working_color_space = "ACEScg"

        self.naming_convention_list = []
        self.naming_convention_list = self.naming_convention_string.split("_")

        #Objects selected when code is excecuted
        self.selected_objects = None

        #This is a placeholder until a path is selected
        self.folder_directory= "Path to the selected."

        self.window_title = "Apply shader with texture maps"
        self.window_title_maya = self.window_title.replace(' ', '_').casefold()

        #Empty list where texture map type checkboxes objects will be appended to
        self.checkboxes_objects_texture_map_types = []

        # List of texture map extensions (filetypes)
        self.ui_dropdown_texture_map_extensions = ['exr', 'tif', 'png', 'jpg', 'jpeg']

        self.ui_checkboxes_texture_map_types = ["basecolor", "metallic", "roughness","emissive", "normal", "height", "transmission"]

        #Close existing window if there is one
        self.window_cleaner()

        "-------------------------------------------------------------------------- BUILDING THE UI -----------------------------------------------------------------------"
        self.window_width = 500
        self.tool_window = cmds.window(self.window_title_maya,
                                       title = self.window_title,
                                       iconName = self.window_title,
                                       widthHeight = (self.window_width,500), sizeable=False, resizeToFitChildren=True)

        cmds.columnLayout(adjustableColumn=True)

        "--------------------------------------------------- ALL THINGS RELATED TO FILE PATH ---------------------------------------------------"
        #Select folder button
        cmds.button(label= "Select Folder", command= self.get_file_path)
        cmds.separator(height=10, style='none')

        self.path_text= cmds.text(f'{self.folder_directory}', align="center", enable= False)
        cmds.separator(height=10, style='none')

        "--------------------------------------------------- ALL THINGS IN UI RELATED TO NAMING ---------------------------------------------------"
        cmds.separator(height=20, style='in')
        cmds.separator(height=20, style='none')

        self.project_code = cmds.textFieldGrp(
            label='Enter the name of the project code: ', placeholderText= "ex. blg11",columnWidth2=(187, 300))
        cmds.separator(height=20, style='none')

        self.asset_library = cmds.textFieldGrp(
            label='Enter the name of the asset library: ', placeholderText= "ex. prop",columnWidth2=(183, 300))
        cmds.separator(height=20, style='none')

        self.asset = cmds.textFieldGrp(
            label='Enter the name of the asset: ', placeholderText="ex. cube", columnWidth2=(148, 300))
        cmds.separator(height=20, style='none')

        self.version = cmds.textFieldGrp(
            label='Enter the version you want to use ', placeholderText="ex. v001", columnWidth2=(177, 300))
        cmds.separator(height=20, style='none')

        # Create a dropdown menu
        self.dropdown_menu_texture_extensions = cmds.optionMenu(label="Choose the file extension of the textures:")

        # Populate the dropdown menu with options
        for option in self.ui_dropdown_texture_map_extensions:
            cmds.menuItem(label=option)

        cmds.separator(height=10, style='none')


        "--------------------------------------------------- ALL THINGS IN UI RELATED TO TEXTURE MAP TYPES ---------------------------------------------------"
        cmds.separator(height=30, style='in')
        cmds.text(
            f'Select what texturetypes need to be used:',
            align="left", enable=True, font = "boldLabelFont")
        cmds.separator(height=10, style='none')

        for name in self.ui_checkboxes_texture_map_types:
            current_checkbox = cmds.checkBoxGrp(label=name,
                                                  columnAttach2=('left', 'left'),
                                                  columnOffset2=(5, 5),
                                                  columnWidth2=(130, 100))
            self.checkboxes_objects_texture_map_types.append(current_checkbox)
            cmds.separator(height=5, style='none')

        "--------------------------------------------------- ALL THINGS IN UI RELATED TO CREATING THE SHADER ---------------------------------------------------"
        cmds.separator(height=20, style='in')

        self.texture_name = cmds.textFieldGrp(
            label='Enter a name for the shader: ', placeholderText="ex. sh_cube", columnWidth2=(150, 300))
        cmds.separator(height=20, style='none')

        #Apply shader to selected object or not
        self.checkbox_apply_shader_to_object= cmds.checkBoxGrp(label= 'Apply created shader to selected object: ',
                                             columnAttach2=('left', 'left'),
                                             columnOffset2= (5,5),
                                             columnWidth2=(250,10))

        cmds.separator(height=10, style='none')
        cmds.separator(height=20, style='in')

        cmds.button(label="Create ai Standard Surface Shader", command = self.get_all_information)

        cmds.showWindow(self.tool_window)


    def window_cleaner(self, *args):
        try:
            if cmds.window(self.window_title_maya, query= True, exists= True):
                cmds.deleteUI(self.window_title_maya, window= True)
                cmds.windowPref(self.window_title_maya, remove= True)
        except:
            pass


    def get_file_path(self, *args):
        self.folder_directory= cmds.fileDialog2(fileMode=3)[0]
        cmds.text(self.path_text,
                  edit= True,
                  label= f'{self.folder_directory}',
                  annotation= self.folder_directory)


    "------------------------------------------------------------- ALL THINGS RELATED TO WHEN CREATE SHADER BUTTON IS PRESSED --------------------------------------------------------------------------------------------"

    def get_all_information(self, *args):
        '''
        get all information from the ui when create shader button is pressed
        :param args: 
        :return: 
        '''

        "-------------------------------------- ALL THINGS RELATED TO FILE PATH -----------------------------------"
        if self.folder_directory == "Path to the selected.":
            self.show_warning_popup("Please select a folder path.")
            cmds.error("Please select a folder path.")

        "---------------------------------- ALL THINGS IN UI RELATED TO NAMING ------------------------------------"

        project_code = cmds.textFieldGrp(self.project_code, query = True, tx = True).lower()
        if project_code == "":
            self.show_warning_popup("Please fill in a project code.")
            cmds.error("Please fill in a project code.")

        asset_library = cmds.textFieldGrp(self.asset_library, query = True, tx = True).lower()
        if asset_library == "":
            self.show_warning_popup("Please fill in an asset library.")
            cmds.error("Please fill in an asset library.")

        asset = cmds.textFieldGrp(self.asset, query = True, tx = True).lower()
        if asset == "":
            self.show_warning_popup("Please fill in an asset")
            cmds.error("Please fill in an asset.")

        version = cmds.textFieldGrp(self.version, query = True, tx = True).lower()
        if asset == "":
            self.show_warning_popup("Please fill in a version")
            cmds.error("Please fill in a version.")

        basename = project_code + "_" + asset_library + "_" + asset + "_texturing" + "_" + version

        #textureset name of the file, later used as shader name
        texture_name = cmds.textFieldGrp(self.texture_name, query = True, tx = True)

        if texture_name ==  "":
            self.show_warning_popup("Please fill in a name for the shader.")
            cmds.error("Please fill in a name for the shader.")

        #Chosen filetype (extension)
        file_extension = cmds.optionMenu(self.dropdown_menu_texture_extensions, query = True, value = True)

        "------------------------------ ALL THINGS IN UI RELATED TO TEXTURE MAP TYPES ------------------------"
        #Selected texture map types
        list_selected_texture_types = []
        for index in range(len(self.checkboxes_objects_texture_map_types)):
            checked = cmds.checkBoxGrp(self.checkboxes_objects_texture_map_types[index], query=True, v1=True)
            if checked:
                list_selected_texture_types.append(self.ui_checkboxes_texture_map_types[index])

        #If the list is empty
        if not list_selected_texture_types:
            self.show_warning_popup("Please select what texture map types need to be imported.")
            cmds.error("Please select what texture map types need to be imported.")

        "----------------------------------- IF APPLY TO SELECTED IS CHECKED ON ----------------------------------"
        #Get the selected objects if there are any
        self.selected_objects = cmds.ls(selection=True)

        "--------------------------------------------------- GET INFORMATION AND CREATE SHADER ---------------------------------------------------"
        list_files_with_correct_extension = self.get_files_with_correct_extension(file_extension)
        list_files_with_correct_basename = self.get_files_with_correct_basename(list_files_with_correct_extension, basename)
        list_files_with_correct_texturetype = self.get_files_with_correct_texturetypes(list_files_with_correct_basename, list_selected_texture_types, basename, file_extension)
        self.create_shader(list_files_with_correct_texturetype, texture_name, file_extension, list_selected_texture_types)


    def get_files_with_correct_extension(self, file_extension):
        '''
        This function will return the filepaths of the files that have the correct extension type.
        :param file_extension: the filetype/extension of the files that need to be used
        :return: a list of filepaths with the correct extension
        '''
        all_file_paths_all_filetypes_list = []
        correct_filetype_files_list = []

        for (path, dirs, files) in os.walk(self.folder_directory):
            for file in files:
                all_file_paths_all_filetypes_list.append(f'{path}/{file}')

        else:
            for item in os.listdir(self.folder_directory):
                if os.path.isfile(f'{self.folder_directory}/{item}'):
                    all_file_paths_all_filetypes_list.append(f'{self.folder_directory}/{item}')

        # Check if the file has the correct extension
        for item in all_file_paths_all_filetypes_list:
                if item.split(".")[-1] == file_extension:
                    correct_filetype_files_list.append(item)

        if not correct_filetype_files_list:
            self.show_warning_popup("There are no files with this extension")
            cmds.error("There are no files with this extension")

        return correct_filetype_files_list

    def get_files_with_correct_basename(self, list_correct_extensions, basename):
        '''
        This function will return the filepaths of the files that have the correct basename.
        :param list_correct_extensions: list of filepaths that have the correct extension
        :param basename: basename of the texture files
        :return: list of filepaths with the correct basename
        '''
        list_correct_basename = []
        list_file_name_for_duplicate_check = []

        #Sorting the filepaths list -> When there are duplicates for filenames, the shortest filepath will be used
        list_correct_extensions.sort()

        for filepath in list_correct_extensions:
            file_name = os.path.basename(filepath)
            if basename in file_name:
                #Making sure there are no duplicates
                if file_name not in list_file_name_for_duplicate_check:
                    list_correct_basename.append(filepath)
                    list_file_name_for_duplicate_check.append(file_name)
        if not list_correct_basename:
            self.show_warning_popup("There are no files with this naming. Please enter a valid project code, assetlibrary, asset and version.")
            cmds.error("There are no files with this naming. Please enter a valid project code, assetlibrary, asset and version.")


        return list_correct_basename

    def get_files_with_correct_texturetypes(self, list_correct_basename, list_chosen_texturetypes, basename, file_extension):

        list_basename_with_texturetype_and_extension = []
        list_files_with_correct_texturetypes = []

        # Sorting the filepaths list -> When there are duplicates for filenames, the shortest filepath will be used
        list_correct_basename.sort()

        for texturetype in list_chosen_texturetypes:
            name = basename + "_" + texturetype + "." + file_extension
            list_basename_with_texturetype_and_extension.append(name)

        for filepath in list_correct_basename:
            file_name = os.path.basename(filepath)
            if file_name in list_basename_with_texturetype_and_extension:
                list_files_with_correct_texturetypes.append(filepath)

        return list_files_with_correct_texturetypes


    def create_shader(self, list_file_paths, shader_name, file_extension, list_selected_texture_types):
        '''
        This function will create the shader and apply it to the object if asked for.
        :param list_dictionaries_information: list with dictionaries for each texture map type selected
        :param shader_name: string with the name for the sahder (= textureset name)
        :return:
        '''

        list_imported_texture_types = []
        list_acescg_extensions = ['exr', 'tif']

        #set the color space to ACEScg if the extension type is exr or tiff, otherwise it's sRGB
        if file_extension in list_acescg_extensions:
            colorspace = "ACEScg"
        else:
            colorspace = "sRGB"

        # Create aiStandardSurface shader
        if not cmds.objExists(shader_name):
            shader = cmds.shadingNode('aiStandardSurface', asShader=True, name=shader_name)
            shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f"{shader_name}SG")
            cmds.connectAttr(f"{shader}.outColor", f"{shading_group}.surfaceShader")

        else:
            shader = shader_name

        for filepath in list_file_paths:

            file_name = os.path.basename(filepath)
            name_without_ext = os.path.splitext(file_name)[0]  # removes .exr
            parts = name_without_ext.split('_')
            texture_type = parts[-1]
            list_imported_texture_types.append(texture_type)

            # Create a file node
            file_node = cmds.shadingNode('file', asTexture=True, name=f"{texture_type}_file")
            place2d_node = cmds.shadingNode('place2dTexture', asUtility=True, name=f"{texture_type}_place2dTexture")

            # Connect place2dTexture to file
            cmds.connectAttr(f"{place2d_node}.outUV", f"{file_node}.uvCoord")
            cmds.connectAttr(f"{place2d_node}.coverage", f"{file_node}.coverage")

            # Set file attributes
            cmds.setAttr(f"{file_node}.fileTextureName", filepath, type="string")



            # Connect file node to shader based on texturetype
            if texture_type == "basecolor":
                cmds.setAttr(f"{file_node}.colorSpace", colorspace, type="string")
                cmds.connectAttr(f"{file_node}.outColor", f"{shader}.baseColor", force=True)

            elif texture_type == "metallic":
                cmds.setAttr(f"{file_node}.colorSpace", "Raw", type="string")
                cmds.connectAttr(f"{file_node}.outAlpha", f"{shader}.metalness", force=True)
                cmds.setAttr(f"{file_node}.alphaIsLuminance", 1)

            elif texture_type == "roughness":
                cmds.setAttr(f"{file_node}.colorSpace", "Raw", type="string")
                cmds.connectAttr(f"{file_node}.outAlpha", f"{shader}.specularRoughness", force=True)
                cmds.setAttr(f"{file_node}.alphaIsLuminance", 1)

            if texture_type == "normal":

                # Create an aiNormalMap node for normal mapping (Arnold shaders)
                normal_map_node = cmds.shadingNode('aiNormalMap', asUtility=True)
                # Rename the aiNormalMap node using the textureset name
                normal_map_node = cmds.rename(normal_map_node, f"{shader_name}_aiNormalMap")
                # Connect the file texture to the normal map node
                cmds.connectAttr(f"{file_node}.outColor", f"{normal_map_node}.input", force=True)
                # Connect the normal map node to the shader's normalCamera input
                cmds.connectAttr(f"{normal_map_node}.outValue", f"{shader}.normalCamera", force=True)


            elif texture_type == "height":
                cmds.setAttr(f"{file_node}.colorSpace", "Raw", type="string")
                # Create a displacement shader node
                displacement_node = cmds.shadingNode('displacementShader', asShader=True)

                # Rename the displacement shader using the textureset name
                displacement_node = cmds.rename(displacement_node, f"{shader_name}_displacementShader")

                # Connect the file node to the displacement shader
                cmds.connectAttr(f"{file_node}.outAlpha", f"{displacement_node}.displacement", force=True)
                cmds.setAttr(f"{file_node}.alphaIsLuminance", 1)

                # Connect the displacement shader to the shading group
                shading_group = cmds.listConnections(shader, type='shadingEngine')

                if shading_group:
                    cmds.connectAttr(f"{displacement_node}.displacement", f"{shading_group[0]}.displacementShader",
                                     force=True)

            elif texture_type == "transmission":
                cmds.setAttr(f"{file_node}.colorSpace", colorspace, type="string")
                cmds.connectAttr(f"{file_node}.outColor", f"{shader}.transmissionColor", force=True)


            elif texture_type == "emissive":
                cmds.setAttr(f"{file_node}.colorSpace", colorspace, type="string")
                cmds.connectAttr(f"{file_node}.outColor", f"{shader}.emissionColor", force=True)

        for selected_texture_type in list_selected_texture_types:
            if selected_texture_type not in list_imported_texture_types:
                self.show_warning_popup(f"{selected_texture_type} texture type was not found and is not imported.")


        apply_to_selected = cmds.checkBoxGrp(self.checkbox_apply_shader_to_object, query=True, v1=True)

        if apply_to_selected:
            if self.selected_objects:
                #Check each selected object to ensure it's a geometry object
                for obj in self.selected_objects:
                    # Check if the object is a mesh (geometry object)
                    if cmds.objectType(obj) == "transform" and cmds.listRelatives(obj, shapes=True) and cmds.objectType(
                            cmds.listRelatives(obj, shapes=True)[0]) == "mesh":
                        #Apply the shader to the geometry object


                        # Apply the shader to the selected geometry object
                        cmds.select(obj)
                        cmds.hyperShade(assign=shader)
                    else:
                        self.show_warning_popup(f"{obj} is not a geometry object, shader will not be applied to it.")
            else:
                self.show_warning_popup("No object selected!")
                cmds.error("No object selected!")


    def show_warning_popup(self, warning):

        cmds.confirmDialog(
            title="Warning",  # Title of the popup
            message = warning,  # Warning message
            button=["OK"],  # Button(s) to display
            defaultButton="OK",  # Default selected button
            cancelButton="OK",  # Button to trigger on cancel
            dismissString="OK",  # Dismiss button
            icon="warning"  # Warning icon
        )

ShaderWithSelectedTextures()