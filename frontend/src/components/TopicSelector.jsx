import React, { useEffect, useRef } from "react";
import AssistLeg from "./AssistLeg.png";

const topics = [
  { id: "constitucion_vs", name: "Constitución" },
  { id: "codigo_trabajo_vs", name: "Código Sustantivo del Trabajo" },
  { id: "reglamentos_vs", name: "Reglamentos Universitarios" }
];

export default function TopicSelector({ onSelect }) {
  const theme = {
    bg: "#0d1117",
    text: "#e6edf3",
    softText: "#9da5b4",
    blue: "#007bff",
    blueHover: "#0063cc"
  };

  //  CAPA QUE SIGUE EL MOUSE
  const glowRef = useRef(null);

  useEffect(() => {
    const glow = glowRef.current;

    const handleMouseMove = (e) => {
      const x = e.clientX;
      const y = e.clientY;

      glow.style.left = `${x}px`;
      glow.style.top = `${y}px`;
    };

    window.addEventListener("mousemove", handleMouseMove);
    return () => window.removeEventListener("mousemove", handleMouseMove);
  }, []);

  return (
    <div
      style={{
        minHeight: "100vh",
        width: "100%",
        overflowX: "hidden",
        background: theme.bg,
        color: theme.text,
        fontFamily: "Inter, sans-serif",
        position: "relative",
        padding: "40px 25px",

        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      {/*  PARTICULAS DEL FONDO */}
      <div className="particle-field"></div>

      {/*  GLOW QUE SIGUE EL MOUSE */}
      <div
        ref={glowRef}
        style={{
          position: "absolute",
          width: 350,
          height: 350,
          background: "radial-gradient(circle, rgba(0,123,255,0.18), transparent 70%)",
          borderRadius: "50%",
          pointerEvents: "none",
          transform: "translate(-50%, -50%)",
          transition: "0.05s",
          filter: "blur(45px)"
        }}
      />

      {/* CONTENIDO */}
      <div
        style={{
          maxWidth: 850,
          textAlign: "center",
          animation: "fadeIn 1s ease"
        }}
      >
        {/* LOGO + TITULO */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            marginBottom: 45
          }}
        >
          <img
            src={AssistLeg}
            alt="AssistLeg logo"
            style={{
              width: 140,
              height: 140,
              objectFit: "contain",
              marginBottom: 15,
              filter: "drop-shadow(0 0 10px rgba(0,0,0,0.5))",
              transition: "0.3s",
            }}
            onMouseOver={(e) => (e.currentTarget.style.transform = "scale(1.07)")}
            onMouseOut={(e) => (e.currentTarget.style.transform = "scale(1)")}
          />

          <h1 style={{ fontSize: 38, margin: 0, fontWeight: "bold" }}>
            AssistLeg
          </h1>

          <p
            style={{
              marginTop: 10,
              fontSize: 18,
              color: theme.softText,
              maxWidth: 700,
              lineHeight: 1.5
            }}
          >
            Tu asistente jurídico impulsado por IA.  
            Interpretación normativa clara, precisa y en tiempo real.
          </p>
        </div>

        {/* SECCIÓN DE TEMAS */}
        <h2 style={{ fontSize: 26, marginBottom: 25 }}>
          Selecciona un área normativa
        </h2>

        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: 18,
            maxWidth: 500,
            margin: "0 auto"
          }}
        >
          {topics.map((t) => (
            <button
              key={t.id}
              onClick={() => onSelect(t.id)}
              style={{
                background: theme.blue,
                border: "none",
                padding: "16px 22px",
                borderRadius: 12,
                color: "white",
                fontSize: 18,
                cursor: "pointer",
                textAlign: "left",
                width: "100%",
                boxShadow: "0px 3px 12px rgba(0,0,0,0.3)",
                transition: "0.25s"
              }}
              onMouseOver={(e) => {
                e.currentTarget.style.background = theme.blueHover;
                e.currentTarget.style.transform = "translateY(-2px) scale(1.02)";
                e.currentTarget.style.boxShadow = "0px 5px 16px rgba(0,0,0,0.45)";
              }}
              onMouseOut={(e) => {
                e.currentTarget.style.background = theme.blue;
                e.currentTarget.style.transform = "translateY(0) scale(1)";
                e.currentTarget.style.boxShadow = "0px 3px 12px rgba(0,0,0,0.3)";
              }}
            >
              {t.name}
            </button>
          ))}
        </div>
      </div>

      {/* ANIMACIONES + PARTICULAS */}
      <style>
        {`
          @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
          }

          /*  PARTICLE FIELD */
          .particle-field {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            z-index: -1;
          }

          .particle-field::before,
          .particle-field::after {
            content: "";
            position: absolute;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.06) 1px, transparent 1px);
            background-size: 40px 40px;
            animation: drift 35s linear infinite;
            opacity: 0.25;
          }

          .particle-field::after {
            animation-duration: 60s;
            background-size: 60px 60px;
            opacity: 0.15;
          }

          @keyframes drift {
            from { transform: translate(0, 0); }
            to { transform: translate(-50%, -50%); }
          }
        `}
      </style>
    </div>
  );
}
