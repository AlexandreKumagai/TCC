# -*- coding: utf-8 -*-
opt = {
    'path_csv': 'download/danbooru-targets.csv',
    'download_img': True,
    'path_download': 'download/imagens/',
    'categoria': 'car'
}

from pycocotools.coco import COCO
import csv
import json

annFiles=[[r'json/instances_train2017.json', r'json/captions_train2017.json', 'train'],
          [r'json/instances_val2017.json', r'json/captions_val2017.json', 'captions']]
categoria = opt['categoria']

dados = {}
dados['info'] = {
      "description": "COCO 2017 Dataset",
      "url": "http://cocodataset.org",
      "version": "1.0",
      "year": 2017,
      "contributor": "COCO Consortium",
      "date_created": "2017/09/01"
  }
dados["images"] = []
dados["annotations"] = []

for annFile in annFiles:
  coco=COCO(annFile[0])

  catIds = coco.getCatIds(catNms=[categoria])
  imgIds = coco.getImgIds(catIds=catIds)
  imagens = coco.loadImgs(ids=imgIds)

  # initialize COCO api for instance annotations
  coco=COCO(annFile[1])

  #buscando anotações
  anotacoes_id = coco.getAnnIds(imgIds=imgIds)
  anotacoes = coco.loadAnns(ids=anotacoes_id)

  #000000581887.jpg
  #gravando anotações em um csv
  gravador_anotacoes = csv.writer(open(opt['path_csv'], mode = 'a'))
  valor_images = {}
  
  for imagem in imagens:      
      valor_images[imagem.get("id")] = imagem.get("file_name")
  
  for anot in anotacoes:
    imagem = valor_images[anot.get('image_id')]
    gravador_anotacoes.writerow([imagem,anot.get('caption')])
  
  if opt['download_img'] == True:
    coco.download(tarDir=opt['path_download'], imgIds=imgIds)
