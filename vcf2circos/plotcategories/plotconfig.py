#!/usr/local/bin/python3

"""
aim: Epurate module and func, handle parameters of circos plot
"""

from functools import lru_cache
import re
import json
import os
import pandas as pd

from vcf2circos.vcfreader import VcfReader
from os.path import join as osj
from tqdm import tqdm
from vcf2circos.utils import variants_color
from pprint import pprint


class Plotconfig(VcfReader):
    """
    Options regroup options passed in args in json file otherwise
    it will be a empty dict,
    All func based on vcf input
    """

    def __init__(
        self,
        filename: str,
        options: dict,
        show: bool,
        file: dict,
        radius: dict,
        sortbycolor: bool,
        colorcolumn: int,
        hovertextformat: dict,
        trace_car: dict,
        data: list,
        layout: dict,
    ):
        super().__init__(filename, options)
        self.default_options = json.load(
            open("../demo_data/options.general.json", "r",)
        )
        if not self.options.get("General", {}).get("title", None):
            self.options["General"]["title"] = os.path.basename(
                self.get_metadatas().get("filename", "myCircos")
            )
        self.show = self.cast_bool(show)
        self.file = file
        self.radius = radius
        self.sortbycolor = self.cast_bool(sortbycolor)
        self.colorcolumn = colorcolumn
        self.hovertextformat = hovertextformat
        self.trace_car = trace_car
        self.data = self.process_vcf()
        self.layout = layout
        self.refgene_genes = osj(
            self.options["Static"],
            "Assembly",
            self.options["Assembly"],
            "genes." + self.options["Assembly"] + "sorted.txt",
        )
        self.refgene_exons = osj(
            self.options["Static"],
            "Assembly",
            self.options["Assembly"],
            "exons." + self.options["Assembly"] + ".txt.gz",
        )

    @staticmethod
    def cast_bool(value: bool) -> str:
        if value:
            return "True"
        else:
            return "False"

    def get_file_features():
        pass

    def get_snvindels_overlapping_sv(self):
        pass

    def vcf_options_default(self):
        pass

    def get_json(self) -> dict:
        """
        last func to be called, passed to Figure class to generate circos plot (main)
        """

        variants_position = (
            self.options.get("Variants", {}).get("rings", {}).get("position", 0.5)
        )
        variants_ring_height = (
            self.options.get("Variants", {}).get("rings", {}).get("height", 0.04)
        )
        variants_ring_space = (
            self.options.get("Variants", {}).get("rings", {}).get("space", 0.01)
        )

        pass

    def process_vcf(self) -> dict:
        """
        Process Just one time vcf variants in a dict which contains all required informations for all type of var used after,
        Act as a plotconfig main\n
        From vcfreader antony explode_category_file_dict_into_dataframe
        """
        data = {
            "Chromosomes": [],
            "Genes": [],
            "Exons": [],
            "Record": [],
            "Variants": [],
            "Variants_type": [],
            "CopyNumber": [],
            "Color": [],
        }
        # VCF parsed file from PyVCF3
        for record in self.vcf_reader:
            # particular process for breakend
            if self.get_copynumber_type(record)[0] in ["BND", "TRA"]:
                pass
                # self.compute_breakend()
            else:
                # print(record.INFO["SV"])
                data["Chromosomes"].append(self.chr_adapt(record))
                data["Genes"].append(self.get_genes_var(record))
                data["Exons"].append("")
                # TODO exons time consumming
                data["Record"].append(record)
                data["Variants"].append(record.INFO)
                svtype, copynumber = self.get_copynumber_type(record)
                data["Variants_type"].append(svtype)
                data["CopyNumber"].append(copynumber)
                data["Color"].append(variants_color[svtype])
        # pprint(data)
        # test
        # def replace_(dico):
        #    rep = ""
        #    excl = ["None", None]
        #    for
        #
        return data

    def chr_adapt(self, record: object) -> str:
        try:
            re.match(r"[0-9]", record.CHROM).group()
            return "chr" + record.CHROM
        except AttributeError:
            return record.CHROM

    def compute_breakend(self):
        # TODO
        pass

    def get_copynumber_type(self, record: object) -> tuple:
        """
        take VCF variant object and return variant type and number of copy in tuple
        REQUIRED monosample vcf
        """
        alt = str(record.ALT[0])
        # checking if CopyNumber annotation in info field
        if record.INFO.get("SVTYPE", ""):
            svtype = record.INFO.get("SVTYPE", "")
            return (svtype, self.get_copynumber_values(svtype, record))
        elif record.INFO.get("SV_type", ""):
            svtype = record.INFO.get("SV_type", "")
            return (svtype, self.get_copynumber_values(svtype, record))
        # It's SV in ALT field
        elif alt.startswith("<"):
            rep = {"<": "", ">": ""}
            svtype = alt
            for key, val in rep.items():
                svtype = svtype.replace(key, val)
            # in case of copy number in alt
            if re.search(r"$[0-9]+", svtype).group():
                copynumber = re.search(r"$[0-9]+", svtype).group()
                return (svtype, copynumber)
            else:
                svtype = svtype.split(":")[0]
                if len(svtype) > 1:
                    copynumber = svtype[1]
                    return (svtype, copynumber)
                else:
                    return (svtype, self.get_copynumber_values(svtype, record))
        else:
            return ("OTHER", 6)

    def get_copynumber_values(self, svtype: str, record: object) -> int:
        """
        take VCF variant object (type of variant could help)and return copynumber as integer from 0 to 5 (which mean 5 or more but in general it 's super rare)\n
        REQUIRED monosample vcf
        """
        if record.INFO.get("CN") is not None:
            return int(record.INFO.get("CN"))
        # list of sample TODO working only if vcf monosample
        else:
            # Need verificatons TODO
            genotype = record.samples[0].data.GT
            if genotype == "1/0" or "0/1":
                gt = 1
            elif genotype == "1/1":
                gt = 2
            else:
                gt = "0/0"

            if svtype in [
                "CNV",
                "INS",
                # "INV",
                # "DEL",
                "DUP",
            ]:
                # CNV or INS
                return gt + 1
            elif svtype == "INV":
                return 2
            elif svtype == "DEL":
                return 2 - gt

    def find_record_gene(self, coord: list, refgene_genes) -> list:
        """
        Greedy, for now need good info in vcf annotations
        """
        gene_list = []
        # only chr for this variants
        refgene_chr = refgene_genes.loc[refgene_genes["chr_name"] == coord[0]]
        for j, rows in refgene_chr.iterrows():
            # variant start begin before a gene and stop inside or after
            if coord[1] <= rows["start"] and (
                coord[2] in range(rows["start"], rows["end"]) or coord[2] >= rows["end"]
            ):
                gene_list.append(rows["gene"])
            # sv only inside one gene
            if coord[1] >= rows["start"] and coord[2] <= rows["end"]:
                gene_list.append(rows["gene"])
            # SV all size done
            if coord[1] <= rows["start"] and coord[2] <= rows["end"]:
                break

        return list(set(gene_list))

    def get_genes_var(self, record: object) -> str:
        refgene_genes = pd.read_csv(
            osj(
                self.options["Static"],
                "Assembly",
                self.options["Assembly"],
                "genes." + self.options["Assembly"] + ".sorted.txt",
            ),
            sep="\t",
            header=0,
            # compression="infer",
        )
        # print(*refgene_genes.columns)
        # .drop_duplicates(subset=["gene"], keep="first")

        gene_name = record.INFO.get("Gene_name")
        if isinstance(gene_name, str):
            return gene_name
        # No Gene_name annotation need to find overlapping gene in sv
        if gene_name is None:
            if record.INFO.get("SVTYPE") not in [
                "BND, TRA",
                "INV",
                None,
            ] or record.INFO.get("SV_type") not in ["BND, TRA", "INV", None]:
                # assert "SVLEN" in record.INFO
                # print(record.INFO["SVLEN"])
                gene_name = self.find_record_gene(
                    [
                        record.CHROM,
                        record.POS,
                        int(record.POS) + int(record.INFO["SVLEN"][0]),
                    ],
                    refgene_genes,
                )
            # SNV indel
            else:
                alternate = int(str(max([len(alt) for alt in list(str(record.ALT))])))
                gene_name = self.find_record_gene(
                    [record.CHROM, record.POS, (int(record.POS) + alternate),],
                    refgene_genes,
                )
                if record.INFO.get("SVTYPE") is None:
                    print(record)
                    print(
                        record.CHROM, record.POS, (int(record.POS) + alternate),
                    )
                    if not gene_name:
                        gene_name = [""]
            return ",".join(gene_name)
