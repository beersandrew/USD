//
// Copyright 2021 Pixar
//
// Licensed under the Apache License, Version 2.0 (the "Apache License")
// with the following modification; you may not use this file except in
// compliance with the Apache License and the following modification to it:
// Section 6. Trademarks. is deleted and replaced with:
//
// 6. Trademarks. This License does not grant permission to use the trade
//    names, trademarks, service marks, or product names of the Licensor
//    and its affiliates, except as required to comply with Section 4(c) of
//    the License and to reproduce the content of the NOTICE file.
//
// You may obtain a copy of the Apache License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the Apache License with the above modification is
// distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied. See the Apache License for the specific
// language governing permissions and limitations under the Apache License.
//
#ifndef PXR_BASE_TF_WRAPTOKEN_H
#define PXR_BASE_TF_WRAPTOKEN_H

#ifdef __EMSCRIPTEN__

#include <emscripten/bind.h>
#include "pxr/base/tf/token.h"
#include "pxr/base/tf/emscriptenTypeRegistration.h"
#include <iostream>

EMSCRIPTEN_REGISTER_TYPE_CONVERSION(pxr::TfToken)
    return BindingType<val>::toWireType(val(value.GetString()));
}
static pxr::TfToken fromWireType(WireType value) {
    return pxr::TfToken(BindingType<val>::fromWireType(value).as<std::string>());
EMSCRIPTEN_REGISTER_TYPE_CONVERSION_END(pxr::TfToken)

EMSCRIPTEN_REGISTER_VECTOR_TO_ARRAY_CONVERSION(pxr::TfToken)
EMSCRIPTEN_REGISTER_TYPE(std::vector<pxr::TfToken>)

#endif // __EMSCRIPTEN__

#endif // PXR_BASE_TF_WRAPTOKEN_H