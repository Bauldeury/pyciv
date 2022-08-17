import client.ArtDefine
import common.Terrain
import common.Feature
import common.Unit


def test_exhaustivity():
    assert "FOG" in client.ArtDefine.tileArtDefines
    assert "UNKNOWN" in client.ArtDefine.tileArtDefines
    assert "UNEXPLORED" in client.ArtDefine.tileArtDefines
    for terrainKey in common.Terrain.terrains:
        assert terrainKey in client.ArtDefine.tileArtDefines
    for featureKey in common.Feature.features:
        assert featureKey in client.ArtDefine.tileArtDefines

    for unitKey in common.Unit.unitTypes:
        assert unitKey in client.ArtDefine.unitArtDefines