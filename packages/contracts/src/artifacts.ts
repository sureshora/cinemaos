export const ARTIFACT_TYPES = [
  "document",
  "image",
  "audio",
  "video",
  "map",
  "historical_record",
  "screenplay",
  "scene",
  "character",
  "music",
  "production_asset",
] as const;

export type ArtifactType = (typeof ARTIFACT_TYPES)[number];

export const ARTIFACT_STATUSES = [
  "draft",
  "ingested",
  "processing",
  "ready",
  "review",
  "approved",
  "rejected",
  "archived",
] as const;

export type ArtifactStatus = (typeof ARTIFACT_STATUSES)[number];

export interface ArtifactSource {
  sourceId: string;
  sourceType: string;
  uri?: string;
  title?: string;
  publisher?: string;
  publishedAt?: string;
  collectedAt: string;
  contentHash?: string;
}

export interface ArtifactLineage {
  parentArtifactIds: string[];
  derivedFrom?: string[];
  operation?: string;
  actor?: string;
  createdAt: string;
}

export interface ArtifactLocation {
  provider: string;
  uri: string;
  mediaType?: string;
  sizeBytes?: number;
}

export interface ArtifactMetadata {
  language?: string;
  languages?: string[];
  country?: string;
  region?: string;
  tags?: string[];
  entityIds?: string[];
  projectId?: string;
  version?: string;
  custom?: Record<string, unknown>;
}

export interface MultimodalArtifact {
  artifactId: string;
  artifactType: ArtifactType;
  status: ArtifactStatus;
  title: string;
  description?: string;
  mediaType: string;
  createdAt: string;
  updatedAt: string;
  location: ArtifactLocation;
  metadata: ArtifactMetadata;
  sources: ArtifactSource[];
  lineage: ArtifactLineage;
  checksum?: string;
  schemaVersion: "1.0";
}
