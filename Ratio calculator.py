class RatioCalculator:
    """Calculates ration PG and VG to mix into E-Liquid"""

    @staticmethod
    def calculate_weights(total_volume_ml: int | float,
                          vg_ratio: int | float,
                          pg_ratio: int | float,
                          vg_density: int | float,
                          pg_density: int | float) -> tuple[int | float, int | float]:
        """Calculate the required weights of VG and PG based on volume and density.

        Args:
            total_volume_ml: Total desired volume in ml
            vg_ratio: Volume percentage of VG
            pg_ratio: Volume percentage of PG
            vg_density: Density of VG in g/ml
            pg_density: Density of PG in g/ml
        Returns:
            Tuple (VG_weight_g, PG_weight_g)"""

        vg_volume_ml = (vg_ratio / 100) * total_volume_ml
        pg_volume_ml = (pg_ratio / 100) * total_volume_ml

        vg_weight_g = vg_volume_ml * vg_density
        pg_weight_g = pg_volume_ml * pg_density

        return vg_weight_g, pg_weight_g


# Example usage
total_volume_ml = 300  # Desired total volume
vg_ratio = 70  # VG percentage
pg_ratio = 30  # PG percentage
vg_density = 1.26  # Example density of VG in g/ml
pg_density = 1.04  # Example density of PG in g/ml

vg_weight, pg_weight = RatioCalculator.calculate_weights(total_volume_ml,
                                                         vg_ratio,
                                                         pg_ratio,
                                                         vg_density,
                                                         pg_density)

print(f"VG Weight: {vg_weight} g")
print(f"PG Weight: {pg_weight} g")
print(f"Total weight: {pg_weight + vg_weight} g")
