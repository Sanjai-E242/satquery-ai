import re
from typing import Dict, Any, List

class QueryParser:
    """
    Parses natural-language queries into structured task intent.
    """
    @staticmethod
    def parse_query(query: str, mode: str = "single") -> Dict[str, Any]:
        q_lower = query.lower()

        # Intent detection logic
        intent = "vqa"
        target = "land_cover"
        requested_outputs = ["text_answer", "confidence"]

        if any(w in q_lower for w in ["highlight", "locate", "where is", "find", "show me", "segment", "bounding box", "mask"]):
            intent = "grounding"
            requested_outputs.extend(["bounding_box", "segmentation_mask"])
            if "water" in q_lower: target = "water_body"
            elif "building" in q_lower or "built-up" in q_lower: target = "built_up_area"
            elif "forest" in q_lower or "tree" in q_lower or "vegetation" in q_lower: target = "vegetation"
            elif "road" in q_lower: target = "road_network"
            else: target = "specified_object"

        elif mode == "bi_temporal" or any(w in q_lower for w in ["change", "changed", "increased", "decreased", "before", "after", "temporal", "difference"]):
            intent = "change_analysis"
            requested_outputs.extend(["change_map", "changed_regions"])
            if "built-up" in q_lower or "building" in q_lower or "urban" in q_lower:
                target = "built_up_change"
            elif "water" in q_lower:
                target = "water_change"
            elif "forest" in q_lower or "deforestation" in q_lower:
                target = "forest_change"
            else:
                target = "general_change"

        elif mode == "optical_sar" or any(w in q_lower for w in ["sar", "optical", "cross-modal", "multimodal", "radar", "together", "fusion"]):
            intent = "optical_sar_fusion"
            requested_outputs.extend(["optical_evidence", "sar_evidence", "fused_map"])
            if "water" in q_lower and "built" in q_lower:
                target = "water_and_built_up"
            elif "water" in q_lower:
                target = "water_body"
            elif "built" in q_lower:
                target = "built_up_area"
            else:
                target = "multimodal_land_cover"

        elif any(w in q_lower for w in ["describe", "caption", "scene", "summary", "overview"]):
            intent = "captioning"
            requested_outputs.append("scene_description")

        return {
            "raw_query": query,
            "intent": intent,
            "target": target,
            "requested_outputs": requested_outputs,
            "analysis_mode": mode
        }
