# @Copyright: CEA-LIST/DIASI/SIALV/LVA (2023)
# @Author: CEA-LIST/DIASI/SIALV/LVA <pixano@cea.fr>
# @License: CECILL-C
#
# This software is a collaborative computer program whose purpose is to
# generate and explore labeled data for computer vision applications.
#
# This software is governed by the CeCILL-C license under French law and
# abiding by the rules of distribution of free software. You can use,
# modify and/ or redistribute the software under the terms of the CeCILL-C
# license as circulated by CEA, CNRS and INRIA at the following URL
#
# http://www.cecill.info

from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import Page, Params
from fastapi_pagination.api import add_pagination

from pixano.api import (
    ItemFeatures,
    Settings,
    load_dataset,
    load_dataset_list,
    load_dataset_stats,
    load_item_embeddings,
    load_item_objects,
    load_items,
    save_item_objects,
)
from pixano.core import ObjectAnnotation
from pixano.data import DatasetInfo, EmbeddingDataset, InferenceDataset


def create_app(settings: Settings = Settings()) -> FastAPI:
    """Run Pixano app

    Args:
        settings (Settings): Dataset Library

    Raises:
        HTTPException: 404, Dataset is not found
        HTTPException: 404, Dataset stats are not found
        HTTPException: 404, Dataset is not found
        HTTPException: 404, Dataset is not found
        HTTPException: 404, Embedding dataset is not found

    Returns:
        FastAPI: Explorer app
    """

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Check if library exists
    if not settings.data_dir.exists():
        raise FileNotFoundError(
            f"Dataset library '{settings.data_dir.absolute()}' not found"
        )

    # Create models folder
    model_dir = settings.data_dir / "models"
    model_dir.mkdir(exist_ok=True)
    app.mount("/models", StaticFiles(directory=model_dir), name="models")

    @app.get("/datasets", response_model=list[DatasetInfo])
    async def get_dataset_list():
        # Load dataset list
        return load_dataset_list(settings)

    @app.get("/datasets/{ds_id}", response_model=DatasetInfo)
    async def get_dataset(ds_id: str):
        # Load dataset
        ds = load_dataset(ds_id, settings)
        if ds is None:
            raise HTTPException(status_code=404, detail="Dataset not found")
        else:
            return ds.info

    @app.get("/datasets/{ds_id}/items", response_model=Page[ItemFeatures])
    async def get_dataset_items(ds_id: str, params: Params = Depends()):
        # Load dataset
        ds = load_dataset(ds_id, settings)
        if ds is None:
            raise HTTPException(status_code=404, detail="Dataset not found")
        else:
            # Load dataset items
            res = load_items(ds, params)
            if res is None:
                raise HTTPException(status_code=404, detail="Dataset items not found")
            else:
                return res

    @app.get("/datasets/{ds_id}/stats")
    async def get_dataset_stats(ds_id: str):
        # Load dataset
        ds = load_dataset(ds_id, settings)
        if ds is None:
            raise HTTPException(status_code=404, detail="Dataset not found")
        else:
            # Load dataset stats
            stats = load_dataset_stats(ds, settings)
            if stats is None:
                raise HTTPException(status_code=404, detail="Dataset stats not found")
            else:
                return stats

    @app.get("/datasets/{ds_id}/items/{item_id}/objects")
    async def get_item_objects(ds_id: str, item_id: str):
        # Load dataset
        ds = load_dataset(ds_id, settings)
        if ds is None:
            raise HTTPException(status_code=404, detail="Dataset not found")

        # Load inference datasets
        inf_datasets = []
        for inf_json in sorted(list(ds.path.glob("db_infer_*/infer.json"))):
            inf_datasets.append(InferenceDataset(inf_json.parent))

        # Return item details
        return load_item_objects(ds, item_id, ds.media_dir, inf_datasets)

    @app.post("/datasets/{ds_id}/items/{item_id}/embeddings")
    async def get_item_embeddings(ds_id: str, item_id: str):
        # Load dataset
        ds = load_dataset(ds_id, settings)
        if ds is None:
            raise HTTPException(status_code=404, detail="Dataset not found")

        # Load embedding dataset (currently selecting latest one)
        emb_ds = None
        for emb_json in sorted(list(ds.path.glob("db_embed_*/embed.json"))):
            emb_ds = EmbeddingDataset(emb_json.parent)
        if emb_ds is None:
            raise HTTPException(status_code=404, detail="Embedding dataset not found")

        # Return item embedding
        return Response(content=load_item_embeddings(emb_ds, item_id))

    @app.post(
        "/datasets/{ds_id}/items/{item_id}/objects",
        response_model=list[ObjectAnnotation],
    )
    async def post_item_objects(
        ds_id: str,
        item_id: str,
        annotations: list[ObjectAnnotation],
    ):
        # Load dataset
        ds = load_dataset(ds_id, settings)
        if ds is None:
            raise HTTPException(status_code=404, detail="Dataset not found")

        # Update dataset annotations
        save_item_objects(ds, item_id, annotations)

        return Response()

    add_pagination(app)

    return app
