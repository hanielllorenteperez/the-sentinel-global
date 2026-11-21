import { Composition } from "remotion";
import { NoticiaRapida, NR_FPS, NOTICIA_EJEMPLO, calcularNoticia } from "./NoticiaRapida";

export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="NoticiaRapida" component={NoticiaRapida} durationInFrames={300} fps={NR_FPS} width={1920} height={1080} defaultProps={NOTICIA_EJEMPLO} calculateMetadata={calcularNoticia} />
    <Composition id="NoticiaRapidaShort" component={NoticiaRapida} durationInFrames={300} fps={NR_FPS} width={1080} height={1920} defaultProps={NOTICIA_EJEMPLO} calculateMetadata={calcularNoticia} />
  </>
);
