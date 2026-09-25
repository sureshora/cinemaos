import type { MultimodalArtifact } from "./artifacts";

export interface ArtifactCreateRequest {
  artifactType: MultimodalArtifact["artifactType"];
  title: string;
  description?: string;
  mediaType: string;
  location: MultimodalArtifact["location"];
  metadata?: MultimodalArtifact["metadata"];
  sources?: MultimodalArtifact["sources"];
  lineage?: Partial<MultimodalArtifact["lineage"]>;
}

export interface ArtifactSearchRequest {
  artifactTypes?: MultimodalArtifact["artifactType"][];
  entityIds?: string[];
  projectId?: string;
  language?: string;
  status?: MultimodalArtifact["status"][];
  query?: string;
}

export interface ArtifactProcessingEvent {
  eventId: string;
  artifactId: string;
  eventType:
    | "ingested"
    | "transcoded"
    | "transcribed"
    | "ocr_completed"
    | "embedded"
    | "classified"
    | "derived"
    | "reviewed"
    | "approved"
    | "rejected";
  occurredAt: string;
  actor: string;
  inputArtifactIds: string[];
  outputArtifactIds: string[];
  metadata?: Record<string, unknown>;
}

export function isArtifact(value: unknown): value is MultimodalArtifact {
  if (!value || typeof value !== "object") return false;
  const item = value as Partial<MultimodalArtifact>;
  return (
    typeof item.artifactId === "string" &&
    typeof item.title === "string" &&
    typeof item.mediaType === "string" &&
    typeof item.createdAt === "string" &&
    typeof item.updatedAt === "string" &&
    typeof item.location === "object" &&
    item.schemaVersion === "1.0"
  );
}
