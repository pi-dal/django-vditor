import {Constants} from "../constants";
import {addScript} from "../util/addScript";
import {mermaidRenderAdapter} from "./adapterRender";
import {genUUID} from "../util/function";

declare const mermaid: {
    initialize(options: any): void,
    render(id: string, text: string): { svg: string }
};

export const mermaidRender = (element: (HTMLElement | Document) = document, cdn = Constants.CDN, theme: string) => {
    const mermaidElements = mermaidRenderAdapter.getElements(element);
    if (mermaidElements.length === 0) {
        return;
    }
    addScript(`${cdn}/dist/js/mermaid/mermaid.min.js?v=11.6.0`, "vditorMermaidScript").then(() => {
        const config: any = {
            securityLevel: "loose", // 升级后无 https://github.com/siyuan-note/siyuan/issues/3587，可使用该选项
            altFontFamily: "sans-serif",
            fontFamily: "sans-serif",
            startOnLoad: false,
            flowchart: {
                htmlLabels: true,
                useMaxWidth: !0
            },
            sequence: {
                useMaxWidth: true,
                diagramMarginX: 8,
                diagramMarginY: 8,
                boxMargin: 8,
                showSequenceNumbers: true // Mermaid 时序图增加序号 https://github.com/siyuan-note/siyuan/pull/6992 https://mermaid.js.org/syntax/sequenceDiagram.html#sequencenumbers
            },
            gantt: {
                leftPadding: 75,
                rightPadding: 20
            }
        };
        if (theme === "dark") {
            config.theme = "dark";
        }
        mermaid.initialize(config);
        mermaidElements.forEach(async (item) => {
            const code = mermaidRenderAdapter.getCode(item);
            if (item.getAttribute("data-processed") === "true" || code.trim() === "") {
                return;
            }
            const id = "mermaid" + genUUID()
            try {
                const mermaidData = await mermaid.render(id, item.textContent);
                item.innerHTML = mermaidData.svg;
            } catch (e) {
                const errorElement = document.querySelector("#" + id);
                item.innerHTML = `${errorElement.outerHTML}<br>
<div style="text-align: left"><small>${e.message.replace(/\n/, "<br>")}</small></div>`;
                errorElement.parentElement.remove();
            }
            item.setAttribute("data-processed", "true");
        });
    });
};
