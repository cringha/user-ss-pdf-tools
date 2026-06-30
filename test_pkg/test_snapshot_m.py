import os

from parser.parser_manager import get_processor_by_city_name


def test_changchun(parent_data_dir, output_image_dir):
    city_name = "长春"
    file_name = f"{city_name}.pdf"
    full_file_path = os.path.join(parent_data_dir, file_name)
    user_name = "唐啸"
    f = get_processor_by_city_name(city_name, output_dir=output_image_dir)

    result1 = f.snapshot_user(full_file_path, user_name)
    assert result1 == True


def test_chang_sha(parent_data_dir, output_image_dir):
    city_name = "长沙"
    file_name = f"{city_name}.pdf"
    full_file_path = os.path.join(parent_data_dir, file_name)
    user_name = "万达"
    f = get_processor_by_city_name(city_name, output_dir=output_image_dir)

    result1 = f.snapshot_user(full_file_path, user_name)
    assert result1 == True


def test_city_xxxx(parent_data_dir, output_image_dir, city_name, user_name):
    # city_name = "长沙"
    file_name = f"{city_name}.pdf"
    full_file_path = os.path.join(parent_data_dir, file_name)
    # user_name = "万达"
    f = get_processor_by_city_name(city_name, output_dir=output_image_dir)

    result1 = f.snapshot_user(full_file_path, user_name)
    assert result1 == True


if __name__ == "__main__":
    parent_data_dir = "../data"
    output_image_dir = "../tmp_test_data"
    #
    # test_changchun(parent_data_dir, output_image_dir)
    # test_city_xxxx(parent_data_dir, output_image_dir, "长春", "唐啸")

    #     "长沙"
    # test_chang_sha(parent_data_dir, output_image_dir)
    # test_city_xxxx(parent_data_dir, output_image_dir, "长沙" ,"万达" )
    # test_city_xxxx(parent_data_dir, output_image_dir, "长沙", "刘畅")

    #    成都
    # test_city_xxxx(parent_data_dir, output_image_dir, "成都" ,"陆诗杰" )
    # test_city_xxxx(parent_data_dir, output_image_dir, "成都", "周兴友")

    #    重庆
    # test_city_xxxx(parent_data_dir, output_image_dir, "重庆" ,"胡凤" )
    # test_city_xxxx(parent_data_dir, output_image_dir, "重庆", "余夏")

    #    大连
    # test_city_xxxx(parent_data_dir, output_image_dir, "大连" ,"贾立军" )

    #    福州
    # test_city_xxxx(parent_data_dir, output_image_dir, "福州", "黄闽江")
    # test_city_xxxx(parent_data_dir, output_image_dir, "福州", "林益峰")
    # test_city_xxxx(parent_data_dir, output_image_dir, "福州", "吴建耀")

    #    杭州
    # test_city_xxxx(parent_data_dir, output_image_dir, "杭州", "许巨峰")

    #    合肥
    # test_city_xxxx(parent_data_dir, output_image_dir, "合肥", "王泽发")

    #
    # #    济南
    # test_city_xxxx(parent_data_dir, output_image_dir, "济南", "季斌")
    # test_city_xxxx(parent_data_dir, output_image_dir, "济南", "李月亭")

    #
    #   #    昆明
    #   test_city_xxxx(parent_data_dir, output_image_dir, "昆明", "彭于鑫")
    # #    南昌
    #   test_city_xxxx(parent_data_dir, output_image_dir, "南昌", "章志强")
    #    南京
    # test_city_xxxx(parent_data_dir, output_image_dir, "南京", "姚斌")
    # test_city_xxxx(parent_data_dir, output_image_dir, "南京", "王方圆")
    #    南宁
    # test_city_xxxx(parent_data_dir, output_image_dir, "南宁", "梁良")
    # test_city_xxxx(parent_data_dir, output_image_dir, "南宁", "张传升")

    #    沈阳
    #     test_city_xxxx(parent_data_dir, output_image_dir, "沈阳", "韩易伸")
    #    天津
    #     test_city_xxxx(parent_data_dir, output_image_dir, "天津", "张健")
    #     test_city_xxxx(parent_data_dir, output_image_dir, "天津", "王帅")

    #    武汉
    # test_city_xxxx(parent_data_dir, output_image_dir, "武汉", "王亚辉")
    # test_city_xxxx(parent_data_dir, output_image_dir, "武汉", "张志琪")
    # test_city_xxxx(parent_data_dir, output_image_dir, "武汉", "韩松明")

    #    乌鲁木齐
    #     test_city_xxxx(parent_data_dir, output_image_dir, "乌鲁木齐", "况文豪")

    #    银川
    # test_city_xxxx(parent_data_dir, output_image_dir, "银川", "蔡骏潇")
    # test_city_xxxx(parent_data_dir, output_image_dir, "银川", "计鹏伟")
    # test_city_xxxx(parent_data_dir, output_image_dir, "银川", "蔡小龙")

   #    郑州
    test_city_xxxx(parent_data_dir, output_image_dir, "郑州", "郑竞可")
