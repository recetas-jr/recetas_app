Módulo: recetas_raciones.py

Responsabilidad:
- Calcular cantidades de ingredientes para raciones solicitadas
- Cálculo temporal, no persistente

Regla de cálculo:
cantidad_ajustada = (cantidad_base / racion_base) * raciones_objetivo

Decisiones:
- No se guardan resultados
- No se modifican recetas
- JSON es fuente única de verdad

Integración:
- Llamado desde main.py
- Opción "Cálculo de raciones"