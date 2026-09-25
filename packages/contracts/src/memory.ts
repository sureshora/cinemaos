export const MEMORY_TYPES = [
  "project",
  "session",
  "artifact",
  "decision",
  "character",
  "scene",
  "continuity",
  "production",
  "agent",
] as const;

export type MemoryType = (typeof MEMORY_TYPES)[number];

export const MEMORY_SCOPES = [
  "project",
  "season",
  "episode",
  "scene",
  "artifact",
  "session",
] as const;

export type MemoryScope = (typeof MEMORY_SCOPES)[number];

export interface MemoryRecord {
  memoryId: string;
  memoryType: MemoryType;
  scope: MemoryScope;
  projectId: string;
  title: string;
  content: string;
  entityIds: string[];
  artifactIds: string[];
  parentMemoryIds: string[];
  sourceIds: string[];
  importance: number;
  createdAt: string;
  updatedAt: string;
  expiresAt?: string;
  metadata?: Record<string, unknown>;
  schemaVersion: "1.0";
}

export interface MemoryQuery {
  projectId: string;
  query?: string;
  memoryTypes?: MemoryType[];
  scopes?: MemoryScope[];
  entityIds?: string[];
  artifactIds?: string[];
  limit?: number;
}

export interface MemoryWriteEvent {
  memoryId: string;
  operation: "create" | "update" | "archive";
  actor: string;
  occurredAt: string;
  reason?: string;
}
