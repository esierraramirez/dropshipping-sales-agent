-- Migración: Agregar campos a tabla orders
-- Fecha: 2026-04-20
-- Descripción: Agregar columnas para contexto conversacional y timestamps adicionales

-- Agregar columnas si no existen
ALTER TABLE orders
ADD COLUMN IF NOT EXISTS conversation_notes TEXT NULL,
ADD COLUMN IF NOT EXISTS chat_summary TEXT NULL,
ADD COLUMN IF NOT EXISTS confirmed_at TIMESTAMP NULL,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP NULL;

-- Resultado esperado: Tabla 'orders' actualizada con los nuevos campos
-- Si ya existen, no se crea duplicado debido a IF NOT EXISTS
