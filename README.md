<html><p><a href="https://loko-ai.com/" target="_blank" rel="noopener"> <img style="vertical-align: middle;" src="https://user-images.githubusercontent.com/30443495/196493267-c328669c-10af-4670-bbfa-e3029e7fb874.png" width="8%" align="left" /> </a></p>
<h1>Handwritten</h1><br></html>

**Handwritten** extension extracts textual content from handwritten single text-line images.

The "Handwriting" dashboard allows you to upload images and visualize the detected results:

<p align="center"><img src="https://github.com/loko-ai/yolo_faces/assets/30443495/27008712-e5c1-4bc5-a9f1-a0af8642dddb" width="80%" /></p>

It is based on the <a href="https://huggingface.co/microsoft/trocr-base-handwritten">microsoft/trocr-base-handwritten</a> model.

You can use the **handwritten** component directly into you flow:

<p align="center"><img src="https://github.com/loko-ai/yolo_faces/assets/30443495/06469f76-bbba-4de8-8aaa-e196e44c9538" width="80%" /></p>


The input of the block is the image you want to process, and it returns the extracted text.


## Configuration

In the file *config.json* you can set where to mount your 
**Hugging Face volume** (all the downloaded models will be saved in this directory):

```
{
  "main": {
    "volumes": [
      "/var/opt/huggingface:/root/.cache/huggingface"
    ],
    "gui": {
      "name": "Handwriting"
    }
  }
}
```