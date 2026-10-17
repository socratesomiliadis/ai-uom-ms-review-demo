package edu.ai;

import java.math.BigDecimal;
import java.math.RoundingMode;

final class DiscountRounding {
    private DiscountRounding() {}

    static BigDecimal round(BigDecimal discount) {
        return discount.setScale(2, RoundingMode.HALF_UP);
    }
}
