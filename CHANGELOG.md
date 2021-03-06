Release v1.0.1-beta (2021-02-08)
---------------------------

### Features

- Almost Vditor features
  - Support three editing modes: what you see is what you get (wysiwyg),    instant rendering (ir), split screen preview (sv)
  - Support outline, mathematical formulas, brain maps, charts, flowcharts, Gantt charts, timing charts, staff, multimedia, voice reading, title anchors, code highlighting and copying, graphviz rendering
  - Built-in security filtering, export, task list, multi-platform preview, multi-theme switching, copy to WeChat official account/Zhuhu function
  - Implement CommonMark and GFM specifications, format Markdown and view syntax tree, and support 10+ configurations
  - The toolbar contains 36+ operations. In addition to supporting extensions, you can customize the shortcut keys, prompts, prompt locations, icons, click events, class names, and sub-toolbars in each item.
  - You can use drag and drop, clipboard to paste upload, display real-time upload progress, and support CORS cross-domain upload
  - Pasted HTML is automatically converted to Markdown. If the pasted includes external link pictures, it can be uploaded to the server through the designated interface
  - Support main window size drag and drop, character count
  - Multi-theme support, built-in three sets of black and white themes
  - Multi-language support, built-in Chinese, English, and Korean text localization
  - Support mainstream browsers, friendly to mobile
- The VditorTextField field is provided for the model and can be displayed directly in the django admin.
- The VditorTextFormField is provided for the Form and ModelForm.
- The VditorWidget is provided for the Admin custom widget.